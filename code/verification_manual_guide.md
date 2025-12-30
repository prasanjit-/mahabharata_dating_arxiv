# Manual Verification Guide
## Verifying the 5561 BCE Mahābhārata Dating Claims

---

## 🔭 STELLARIUM (Recommended - Easiest)

### Download & Install
- **Website:** https://stellarium.org/
- **Free** for Windows, Mac, Linux
- **Supports dates:** 100,000 BCE to 100,000 CE

---

### Step-by-Step Verification

#### SETUP
1. Open Stellarium
2. Press `F6` → Location window
3. Search "Kurukshetra" or manually enter:
   - Latitude: **29.97° N**
   - Longitude: **76.83° E**
4. Click "Use as default"

---

#### TEST 1: Arundhati-Vasishtha Configuration

**What to verify:** Alcor appears to "lead" (be west of) Mizar

1. Press `F5` → Date/Time window
2. Enter date: **-5560 / 10 / 16** (this is 5561 BCE)
   - Year: -5560 (Stellarium uses astronomical year numbering)
   - Month: 10
   - Day: 16
   - Time: 20:00
3. Press `F3` → Search for "Mizar"
4. Press `Space` to center on it
5. Zoom in with scroll wheel
6. Look for Alcor (small star nearby)

**Expected Result:**
- In 5561 BCE: Alcor should be **WEST** (right side when facing north) of Mizar
- In 2024 CE: Alcor is **EAST** (left side) of Mizar
- This confirms the "Arundhati leading Vasishtha" observation!

---

#### TEST 2: Solar Eclipse on Day 14 (October 29, 5561 BCE)

1. Press `F5` → Set date to: **-5560 / 10 / 29**
2. Set time to: **16:30** (4:30 PM local)
3. Press `F3` → Search for "Sun"
4. Press `Space` to center
5. Look for the Moon near the Sun

**Expected Result:**
- Moon should be very close to or overlapping the Sun
- This confirms a solar eclipse was possible on Day 14!

**To animate:**
- Press `L` to speed up time
- Watch the Moon approach and cross the Sun

---

#### TEST 3: Mars Retrograde in Capricorn

1. Set date to: **-5560 / 10 / 01**
2. Search for "Mars" (`F3`)
3. Note its position (should be in Sagittarius/Capricorn)
4. Press `=` key to advance one day at a time
5. Watch Mars over 90 days

**Expected Result:**
- Mars should appear to move backward (retrograde) for several weeks
- Position should be in Capricorn region (zodiac shown with `Z` key)

---

#### TEST 4: Planetary Clustering

1. Set date to: **-5560 / 10 / 16**
2. Press `Z` to show zodiac constellations
3. Press `E` to show ecliptic line
4. Locate all 7 classical planets:
   - Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn

**Expected Result:**
- All 7 planets should be within ~180° of sky (6 zodiac signs)

---

#### TEST 5: No Pole Star

1. Set date to: **-5560 / 10 / 16**
2. Look straight up toward North (press `N` then look up)
3. Find the North Celestial Pole

**Expected Result:**
- No bright star at the pole!
- Polaris is far from the pole in this era
- This explains why Mahābhārata never mentions "Dhruva" (pole star)

---

#### TEST 6: Comparison with 3102 BCE

1. Set date to: **-3101 / 10 / 16** (3102 BCE)
2. Repeat Test 1 (Mizar-Alcor)
3. Compare positions

**Expected Result:**
- Alcor should still be west of Mizar (constraint satisfied)
- But other constraints (eclipse, Mars position) won't match!

---

## 🌐 NASA HORIZONS (Web Interface)

### Access
- **URL:** https://ssd.jpl.nasa.gov/horizons/app.html
- **Limitation:** Accuracy decreases before ~3000 BCE

---

### Step-by-Step

1. **Set Target Body:**
   - Click "Edit" next to Target Body
   - Select: Mars (499), Jupiter (599), Saturn (699), etc.

2. **Set Observer Location:**
   - Select "Geocentric" or enter coordinates:
   - Lon: 76.83°, Lat: 29.97°

3. **Set Time:**
   - Start: -5560-Oct-16 (use this format)
   - Stop: -5560-Oct-17
   - Step: 1 day

4. **Select Output:**
   - Check: "Observer ecliptic lon & lat"
   - Check: "RA & DEC"

5. **Click "Generate Ephemeris"**

---

### What to Look For

| Planet | Expected Position (5561 BCE) |
|--------|------------------------------|
| Mars | Sagittarius/Capricorn (~270°-300°) |
| Saturn | Taurus/Rohini region (~40°-60°) |
| Jupiter | Scorpio/Sagittarius (~240°-270°) |

---

## 🐍 PYTHON VERIFICATION

### Install Requirements
```bash
pip install astroquery astropy pandas ephem pyswisseph
```

### Quick Script
```python
# Using Swiss Ephemeris (works for ancient dates)
import swisseph as swe

# Set ephemeris path (download from https://www.astro.com/swisseph/)
swe.set_ephe_path('/path/to/ephe')

# October 16, 5561 BCE
# Julian Day calculation
jd = swe.julday(-5560, 10, 16, 12.0)  # Note: -5560 = 5561 BCE

print(f"Julian Day: {jd}")

# Get planetary positions
planets = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
}

for name, planet_id in planets.items():
    pos = swe.calc_ut(jd, planet_id)
    longitude = pos[0][0]
    print(f"{name}: {longitude:.2f}° (Ecliptic Longitude)")
```

---

## 📊 EXPECTED RESULTS SUMMARY

| Test | Claim | 5561 BCE | 3102 BCE | 1000 BCE |
|------|-------|----------|----------|----------|
| Alcor leads Mizar | ✓ Required | ✅ YES | ✅ YES | ❌ NO |
| Eclipse Day 14 | ✓ Required | ✅ YES | ❌ NO | ❌ NO |
| Mars retrograde | ✓ Required | ✅ YES | ❓ Maybe | ❌ NO |
| Saturn in Rohini | ✓ Required | ✅ YES | ❌ NO | ❌ NO |
| No pole star | ✓ Required | ✅ YES | ✅ YES | ❌ NO |
| 7 planets in 6 signs | ✓ Required | ✅ YES | ❓ Partial | ❌ NO |

**Only 5561 BCE satisfies ALL constraints!**

---

## 🎥 VIDEO TUTORIALS

For visual learners, search YouTube for:
- "Stellarium ancient dates tutorial"
- "Stellarium Mahabharata astronomy"
- "NASA Horizons ancient ephemeris"

---

## ❓ TROUBLESHOOTING

**Q: Stellarium shows different positions than expected?**
- Check you're using astronomical year (-5560 = 5561 BCE)
- Verify location is set to Kurukshetra
- Make sure you're looking at the correct time (evening)

**Q: NASA Horizons gives errors for ancient dates?**
- Horizons has limited accuracy before ~3000 BCE
- Use Stellarium or Swiss Ephemeris instead

**Q: How do I know which star is Alcor vs Mizar?**
- Mizar is brighter (magnitude 2.2)
- Alcor is dimmer (magnitude 4.0)
- They are about 12 arcminutes apart

---

*Verification guide for DOI: 10.5281/zenodo.18100709*
