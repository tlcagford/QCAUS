"""
StealthPDPRadar - PDP Quantum Radar for Stealth Detection
Detects stealth aircraft using dark-mode leakage
"""

import numpy as np
from .pdp_physics import pdp_mixing_angle, pdp_conversion_probability

# Stealth platform signatures
US_STEALTH_PLATFORMS = {
    "F-22 Raptor": {"rcs": 0.0001, "speed": 520, "altitude": 38000, "callsigns": ["AF", "RCH"], "operator": "USAF"},
    "F-35 Lightning II": {"rcs": 0.001, "speed": 550, "altitude": 35000, "callsigns": ["AF", "RCH", "NAVY"], "operator": "USAF/USN/USMC"},
    "B-21 Raider": {"rcs": 0.0005, "speed": 520, "altitude": 40000, "callsigns": ["RCH", "AF"], "operator": "USAF"},
    "B-2 Spirit": {"rcs": 0.0002, "speed": 475, "altitude": 40000, "callsigns": ["RCH"], "operator": "USAF"},
    "NGAD": {"rcs": 0.0003, "speed": 650, "altitude": 45000, "callsigns": ["AF"], "operator": "USAF"}
}

FOREIGN_STEALTH = {
    "Su-57": {"rcs": 0.01, "speed": 520, "altitude": 38000, "operator": "Russian Air Force"},
    "J-20": {"rcs": 0.008, "speed": 530, "altitude": 37000, "operator": "PLAAF"}
}


def detect_stealth_aircraft(aircraft_data, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """
    Detect stealth aircraft using PDP quantum filter
    Returns aircraft with stealth probability and detected platform
    """
    mixing = pdp_mixing_angle(epsilon, B_field, m_dark)
    
    for ac in aircraft_data:
        if ac.get('type') == "Military":
            # Quantum signature strength
            quantum_sig = mixing * 50
            base_prob = min(quantum_sig * 30, 95)
            
            # Determine if US aircraft from callsign
            callsign = ac.get('callsign', '').upper()
            is_us = any(callsign.startswith(p) for p in ['AF', 'RCH', 'NAVY', 'MARINE'])
            
            # Select platform database
            platforms = US_STEALTH_PLATFORMS if is_us else {**US_STEALTH_PLATFORMS, **FOREIGN_STEALTH}
            bonus = 1.2 if is_us else 1.0
            
            # Match against known platforms
            best_match = None
            best_score = 0
            for platform, sig in platforms.items():
                speed_match = 1 - min(abs(ac['speed'] - sig['speed']) / sig['speed'], 1)
                alt_match = 1 - min(abs(ac['altitude'] - sig['altitude']) / sig['altitude'], 1)
                score = (speed_match * 0.6 + alt_match * 0.4) * bonus
                
                if score > best_score:
                    best_score = score
                    best_match = platform
            
            ac['stealth_prob'] = min(base_prob * best_score, 99)
            ac['detected_platform'] = best_match if ac['stealth_prob'] > 20 else None
            ac['is_stealth'] = ac['stealth_prob'] > 20
            ac['operator'] = platforms.get(best_match, {}).get('operator', '') if best_match else ''
    
    return aircraft_data


def generate_radar_return(target_x, target_y, range_km, rcs=0.001, noise_level=0.03):
    """
    Generate simulated radar return for a target
    """
    size = 200
    x = np.linspace(-range_km, range_km, size)
    y = np.linspace(-range_km, range_km, size)
    X, Y = np.meshgrid(x, y)
    
    distance = np.sqrt((X - target_x)**2 + (Y - target_y)**2)
    conventional = rcs * np.exp(-distance**2 / (2 * (range_km/8)**2))
    
    # PDP quantum signature (stronger for stealthier targets)
    quantum_strength = 0.25 * (1 / (rcs + 1e-12)) ** 0.3
    quantum = quantum_strength * np.exp(-distance**2 / (2 * (range_km/5)**2))
    
    noise = np.random.randn(size, size) * noise_level
    radar_data = conventional + quantum + noise
    radar_data = np.clip(radar_data, 0, 1)
    
    return radar_data, conventional, quantum


def pdp_quantum_filter(radar_return, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """
    PDP quantum filter for stealth detection
    Extracts dark-mode leakage from radar returns
    """
    mixing = epsilon * B_field / (m_dark + 1e-12)
    oscillation = np.sin(radar_return * np.pi * 5)
    dark_mode_leakage = radar_return * mixing * oscillation
    enhanced = radar_return + dark_mode_leakage * 0.8
    
    return enhanced, dark_mode_leakage
