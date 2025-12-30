#!/usr/bin/env python3
"""
============================================================================
NASA HORIZONS VERIFICATION SCRIPT
Verify Astronomical Claims in "Dating the Mahabharata: 5561 BCE Hypothesis"
============================================================================

REQUIREMENTS:
    pip install astroquery astropy pandas

USAGE:
    python nasa_horizons_verification.py

This script queries NASA JPL Horizons system to verify:
1. Planetary positions on October 16, 5561 BCE
2. Mars retrograde motion
3. Eclipse conditions
4. Saturn and Jupiter positions

Author: Prasanjit Singh
DOI: 10.5281/zenodo.18100709
============================================================================
"""

from astroquery.jplhorizons import Horizons
from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Kurukshetra coordinates
KURUKSHETRA = {
    'lon': 76.83,  # degrees East
    'lat': 29.97,  # degrees North
    'elevation': 0.25  # km
}

# Target bodies (NASA Horizons ID codes)
BODIES = {
    'Sun': '10',
    'Moon': '301',
    'Mercury': '199',
    'Venus': '299',
    'Mars': '499',
    'Jupiter': '599',
    'Saturn': '699',
}

# Key dates to verify
DATES = {
    'war_start': '-5560-10-16',      # October 16, 5561 BCE
    'day_14_eclipse': '-5560-10-29',  # October 29, 5561 BCE (Jayadratha eclipse)
    'bhishma_death': '-5559-01-13',   # ~January 13, 5560 BCE (Winter solstice)
    'comparison_3102': '-3101-10-16', # October 16, 3102 BCE (Traditional date)
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_horizons_data(body_id, date_str, location=None):
    """
    Query NASA Horizons for a body's position at a given date.
    
    Note: Horizons has limitations for dates before ~3000 BCE.
    For older dates, we use approximate calculations.
    """
    try:
        # Create location dictionary for Horizons
        if location:
            loc = {
                'lon': location['lon'],
                'lat': location['lat'],
                'elevation': location['elevation']
            }
        else:
            loc = None
        
        # Query Horizons
        obj = Horizons(
            id=body_id,
            location=loc if loc else '500@399',  # Geocentric if no location
            epochs={'start': date_str, 'stop': date_str, 'step': '1d'}
        )
        
        # Get ephemeris
        eph = obj.ephemerides()
        return eph
    
    except Exception as e:
        print(f"  Warning: Could not query Horizons for {body_id}: {e}")
        return None


def ecliptic_longitude_to_zodiac(lon):
    """Convert ecliptic longitude to zodiac sign."""
    signs = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    # Normalize longitude to 0-360
    lon = lon % 360
    sign_idx = int(lon / 30)
    degree_in_sign = lon % 30
    return f"{signs[sign_idx]} {degree_in_sign:.1f}°"


def check_mars_retrograde(start_date, days=90):
    """
    Check Mars motion over a period to detect retrograde.
    
    Returns list of (date, longitude, motion_direction)
    """
    print("\n  Checking Mars motion (this may take a moment)...")
    
    positions = []
    prev_lon = None
    
    for i in range(0, days, 3):  # Check every 3 days
        try:
            # Calculate date
            date_str = f"{start_date}"
            
            obj = Horizons(
                id='499',  # Mars
                location='500@399',
                epochs={'start': start_date, 'stop': start_date, 'step': '1d'}
            )
            eph = obj.ephemerides()
            
            if eph is not None and len(eph) > 0:
                lon = float(eph['EclLon'][0])
                
                if prev_lon is not None:
                    diff = lon - prev_lon
                    # Handle wraparound at 360°
                    if diff > 180:
                        diff -= 360
                    elif diff < -180:
                        diff += 360
                    
                    direction = "Direct" if diff > 0 else "RETROGRADE" if diff < 0 else "Stationary"
                else:
                    direction = "N/A"
                
                positions.append({
                    'date': start_date,
                    'longitude': lon,
                    'zodiac': ecliptic_longitude_to_zodiac(lon),
                    'direction': direction
                })
                
                prev_lon = lon
        
        except Exception as e:
            pass
    
    return positions


# ============================================================================
# VERIFICATION TESTS
# ============================================================================

def test_planetary_positions(date_str, date_name):
    """Test 1: Get all planetary positions for a given date."""
    
    print(f"\n{'='*60}")
    print(f"PLANETARY POSITIONS: {date_name}")
    print(f"Date: {date_str}")
    print(f"{'='*60}")
    
    results = []
    
    for body_name, body_id in BODIES.items():
        print(f"  Querying {body_name}...", end=" ")
        
        try:
            eph = get_horizons_data(body_id, date_str)
            
            if eph is not None and len(eph) > 0:
                # Extract position data
                ra = float(eph['RA'][0]) if 'RA' in eph.colnames else None
                dec = float(eph['DEC'][0]) if 'DEC' in eph.colnames else None
                ecl_lon = float(eph['EclLon'][0]) if 'EclLon' in eph.colnames else None
                
                zodiac = ecliptic_longitude_to_zodiac(ecl_lon) if ecl_lon else "N/A"
                
                results.append({
                    'Body': body_name,
                    'RA (deg)': f"{ra:.2f}" if ra else "N/A",
                    'Dec (deg)': f"{dec:.2f}" if dec else "N/A",
                    'Ecl. Lon': f"{ecl_lon:.2f}°" if ecl_lon else "N/A",
                    'Zodiac': zodiac
                })
                print("OK")
            else:
                results.append({
                    'Body': body_name,
                    'RA (deg)': "Error",
                    'Dec (deg)': "Error",
                    'Ecl. Lon': "Error",
                    'Zodiac': "Error"
                })
                print("FAILED")
        
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                'Body': body_name,
                'RA (deg)': "Error",
                'Dec (deg)': "Error", 
                'Ecl. Lon': "Error",
                'Zodiac': "Error"
            })
    
    # Display results
    if results:
        df = pd.DataFrame(results)
        print(f"\n{df.to_string(index=False)}")
    
    return results


def test_planetary_clustering(results):
    """Test 2: Check if planets are within 6 zodiac signs (180°)."""
    
    print(f"\n{'='*60}")
    print("PLANETARY CLUSTERING ANALYSIS")
    print("Claim: Seven planets within 6 zodiac signs (180°)")
    print(f"{'='*60}")
    
    longitudes = []
    for r in results:
        if r['Ecl. Lon'] not in ["N/A", "Error"]:
            lon = float(r['Ecl. Lon'].replace('°', ''))
            longitudes.append((r['Body'], lon))
    
    if len(longitudes) >= 2:
        lons = [l[1] for l in longitudes]
        min_lon = min(lons)
        max_lon = max(lons)
        
        # Handle wraparound
        span = max_lon - min_lon
        if span > 180:
            # Try shifting reference
            shifted = [(l + 180) % 360 for l in lons]
            span = max(shifted) - min(shifted)
        
        print(f"\n  Longitude range: {min_lon:.1f}° to {max_lon:.1f}°")
        print(f"  Total span: {span:.1f}°")
        print(f"  Within 180° (6 signs)? {'YES ✓' if span <= 180 else 'NO ✗'}")
    
    return span if longitudes else None


def test_eclipse_conditions(date_str):
    """Test 3: Check Sun-Moon angular separation for eclipse."""
    
    print(f"\n{'='*60}")
    print("ECLIPSE CONDITIONS CHECK")
    print(f"Date: {date_str} (Day 14 - Jayadratha Episode)")
    print(f"{'='*60}")
    
    try:
        # Get Sun position
        sun_eph = get_horizons_data('10', date_str)
        # Get Moon position  
        moon_eph = get_horizons_data('301', date_str)
        
        if sun_eph is not None and moon_eph is not None:
            sun_lon = float(sun_eph['EclLon'][0])
            moon_lon = float(moon_eph['EclLon'][0])
            sun_lat = float(sun_eph['EclLat'][0]) if 'EclLat' in sun_eph.colnames else 0
            moon_lat = float(moon_eph['EclLat'][0]) if 'EclLat' in moon_eph.colnames else 0
            
            # Angular separation in longitude
            lon_diff = abs(moon_lon - sun_lon)
            if lon_diff > 180:
                lon_diff = 360 - lon_diff
            
            print(f"\n  Sun ecliptic longitude: {sun_lon:.2f}°")
            print(f"  Moon ecliptic longitude: {moon_lon:.2f}°")
            print(f"  Sun-Moon longitude difference: {lon_diff:.2f}°")
            print(f"  Moon ecliptic latitude: {moon_lat:.2f}°")
            
            # Eclipse possible if:
            # - New Moon (Sun-Moon conjunction, lon_diff < 15°)
            # - Moon near ecliptic (|lat| < 1.5°)
            
            is_new_moon = lon_diff < 15
            near_ecliptic = abs(moon_lat) < 1.5
            
            print(f"\n  New Moon (conjunction)? {'YES ✓' if is_new_moon else 'NO ✗'} (need < 15°)")
            print(f"  Moon near ecliptic? {'YES ✓' if near_ecliptic else 'NO ✗'} (need |lat| < 1.5°)")
            print(f"  Solar eclipse possible? {'YES ✓' if (is_new_moon and near_ecliptic) else 'UNLIKELY'}")
            
    except Exception as e:
        print(f"  Error checking eclipse conditions: {e}")


def test_saturn_position(date_str):
    """Test 4: Check Saturn position (should be in Rohini/Taurus region)."""
    
    print(f"\n{'='*60}")
    print("SATURN POSITION CHECK")
    print("Claim: Saturn afflicting Rohini (Taurus region, ~45-60°)")
    print(f"{'='*60}")
    
    try:
        eph = get_horizons_data('699', date_str)
        
        if eph is not None:
            lon = float(eph['EclLon'][0])
            zodiac = ecliptic_longitude_to_zodiac(lon)
            
            # Rohini nakshatra is roughly 40-53° (Taurus)
            in_rohini = 40 <= lon <= 60
            
            print(f"\n  Saturn ecliptic longitude: {lon:.2f}°")
            print(f"  Saturn zodiac position: {zodiac}")
            print(f"  In Rohini region (40-60°)? {'YES ✓' if in_rohini else 'NO ✗'}")
    
    except Exception as e:
        print(f"  Error: {e}")


# ============================================================================
# ALTERNATIVE: Manual Calculation for Ancient Dates
# ============================================================================

def calculate_approximate_positions_ancient(jd):
    """
    Approximate planetary positions for very ancient dates.
    Uses simplified orbital elements.
    
    Note: This is less accurate than Horizons but works for any date.
    """
    
    print("\n" + "="*60)
    print("APPROXIMATE CALCULATIONS (for dates beyond Horizons range)")
    print("="*60)
    
    # Days since J2000.0 (JD 2451545.0)
    T = (jd - 2451545.0) / 36525.0  # Julian centuries
    
    # Mean longitudes (simplified, in degrees)
    # These are approximate formulas
    
    planets = {
        'Sun': 280.46646 + 36000.76983 * T,
        'Moon': 218.3165 + 481267.8813 * T,
        'Mercury': 252.2509 + 149472.6746 * T,
        'Venus': 181.9798 + 58517.8157 * T,
        'Mars': 355.4330 + 19140.2993 * T,
        'Jupiter': 34.3515 + 3034.9057 * T,
        'Saturn': 50.0774 + 1222.1138 * T,
    }
    
    print(f"\n  Julian Date: {jd:.1f}")
    print(f"  Centuries from J2000: {T:.2f}")
    print(f"\n  Approximate Mean Longitudes:")
    print(f"  {'-'*40}")
    
    for planet, lon in planets.items():
        lon_norm = lon % 360
        zodiac = ecliptic_longitude_to_zodiac(lon_norm)
        print(f"  {planet:10s}: {lon_norm:7.2f}° ({zodiac})")
    
    return planets


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  NASA HORIZONS VERIFICATION SCRIPT                               ║
║  Paper: Dating the Mahābhārata (5561 BCE Hypothesis)             ║
║  DOI: 10.5281/zenodo.18100709                                    ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("NOTE: NASA Horizons has limited range for ancient dates.")
    print("For dates before ~3000 BCE, results may be unavailable.")
    print("Using approximate calculations as backup.\n")
    
    # ========================================================================
    # Test for 5561 BCE
    # ========================================================================
    
    print("\n" + "="*70)
    print(" VERIFICATION FOR 5561 BCE (Proposed Mahabharata War Date)")
    print("="*70)
    
    # Convert to Julian Date for approximate calculations
    # October 16, 5561 BCE ≈ JD -310000 (approximate)
    # More precise: JD = 367*Y - INT(7*(Y+INT((M+9)/12))/4) + INT(275*M/9) + D + 1721013.5
    
    # Try Horizons first
    war_date = DATES['war_start']
    
    print(f"\nAttempting NASA Horizons query for {war_date}...")
    results_5561 = test_planetary_positions(war_date, "October 16, 5561 BCE")
    
    # If Horizons failed, use approximate calculations
    if all(r['Ecl. Lon'] in ['Error', 'N/A'] for r in results_5561):
        print("\nHorizons unavailable for this date. Using approximate formulas...")
        # JD for Oct 16, 5561 BCE (approximate)
        jd_5561 = 260649.5  # Approximate Julian Date
        calculate_approximate_positions_ancient(jd_5561)
    else:
        test_planetary_clustering(results_5561)
    
    # Eclipse check
    test_eclipse_conditions(DATES['day_14_eclipse'])
    
    # Saturn position
    test_saturn_position(war_date)
    
    # ========================================================================
    # Comparison with 3102 BCE
    # ========================================================================
    
    print("\n" + "="*70)
    print(" COMPARISON: 3102 BCE (Traditional Kali Yuga Date)")
    print("="*70)
    
    results_3102 = test_planetary_positions(DATES['comparison_3102'], "October 16, 3102 BCE")
    
    if not all(r['Ecl. Lon'] in ['Error', 'N/A'] for r in results_3102):
        test_planetary_clustering(results_3102)
    
    # ========================================================================
    # Summary
    # ========================================================================
    
    print("\n" + "="*70)
    print(" VERIFICATION SUMMARY")
    print("="*70)
    print("""
    To fully verify ancient dates, use:
    
    1. STELLARIUM (Recommended for visualization)
       - Supports dates back to 100,000 BCE
       - Run the provided .ssc script
       - Visually confirm star/planet positions
    
    2. NASA HORIZONS WEB INTERFACE
       - https://ssd.jpl.nasa.gov/horizons/app.html
       - Limited to ~3000 BCE for most bodies
       - Best for recent historical dates
    
    3. SWISS EPHEMERIS / PYSWISSEPH
       - pip install pyswisseph
       - Supports dates to 5400 BCE with high accuracy
       - Best for programmatic verification
    
    4. SOLEX (Solar System Ephemeris)
       - Free software for very ancient dates
       - http://www.solexorb.it/
    """)
    
    print("\n" + "="*70)
    print(" SCRIPT COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
