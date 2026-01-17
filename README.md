# OSK Launcher

A floating, accessible On-Screen Keyboard launcher for Windows 10 Home with verbose terminal output and visual branding.

 Made for 'The Real Handi'
  https://twitch.tv/therealhandi
  
## Features

✅ **Floating Button Interface** - Always-on-top, draggable launcher window  
✅ **Verbose Terminal Output** - See detailed launch logs with visual feedback  
✅ **Accessibility Logo** - Displays branding before launching OSK  
✅ **Multiple Launch Methods** - Tries 4 different approaches to handle system restrictions  
✅ **No External Dependencies** - Uses only Python standard library (after initial tkinter check)  
✅ **Windows 10 Home Compatible** - Works with standard user accounts  

## Installation

### Option A: Run as Python Script

**Requirements:**
- Python 3.7+ installed on your system
- Python added to PATH

**Setup:**
1. Save `osk_launcher.py` to any folder
2. Double-click the file, or run in terminal:
   ```
   python osk_launcher.py
   ```

### Option B: Run as Windows EXE (Recommended)

**Requirements:**
- Python 3.7+ (with pip)
- PyInstaller

**Build the EXE:**
1. Place `osk_launcher.py` and `build_exe.bat` in the same folder
2. Double-click `build_exe.bat`
3. Wait for the build to complete
4. Your EXE will be at: `dist\OSK_Launcher.exe`

You can now:
- Run it directly from `dist\`
- Move it to any location
- Create a desktop shortcut
- Add it to your Startup folder

## Usage

**Python Script:**
```
python osk_launcher.py
```

**EXE:**
- Double-click `OSK_Launcher.exe`

**What happens:**
1. A floating button window appears (draggable, always on top)
2. Click the button
3. Logo displays in a popup
4. Terminal opens showing verbose launch logs
5. On-Screen Keyboard launches
6. Terminal stays open for you to review the output
7. Close the terminal when done

## Controls

| Action | Result |
|--------|--------|
| Left-Click + Drag | Move the floating button |
| Right-Click | Show exit menu |
| ESC key | Close the launcher |
| Click Button | Launch OSK (opens terminal with verbose output) |

## Troubleshooting

### "tkinter not found"
Python's tkinter is missing. Fix by:
1. Go to Settings → Apps → Apps & features
2. Find Python
3. Click "Modify"
4. Check "tcl/tk and IDLE"
5. Click "Install"
6. Restart the script

### OSK Won't Launch
The script tries 4 different methods. Check the terminal output to see which method failed.

**Possible causes:**
- On-Screen Keyboard disabled in Windows
- Account permissions restricted
- System group policy restrictions (common in workplaces)

**To check OSK availability:**
1. Open Settings
2. Go to Apps → Apps & features
3. Search for "Keyboard"
4. Verify "On-Screen Keyboard" is listed and enabled

### Build fails with "PyInstaller not found"
Install PyInstaller manually:
```
pip install pyinstaller
```

Then run the batch file again.

## Files

```
osk_launcher.py          - Main Python script
build_exe.bat            - Batch file to build EXE
dist/OSK_Launcher.exe    - Compiled Windows executable (created after build)
```

## Technical Details

**Language:** Python 3.7+  
**GUI Framework:** tkinter (built into Python)  
**Target OS:** Windows 10 Home and above  
**Build Tool:** PyInstaller  

**No external package dependencies after initial setup** - only uses Python standard library:
- tkinter (GUI)
- subprocess (process management)
- os (file/system access)
- sys (system utilities)
- ctypes (Windows API calls)
- time (delays/timing)

## Accessibility

This tool is designed for accessibility. The On-Screen Keyboard helps users who:
- Cannot use a physical keyboard
- Have motor control difficulties
- Use eye-tracking or switch access devices
- Need alternative input methods

## License

Free to use and modify.

## Support

If the OSK won't launch:
1. Check the terminal output for error messages
2. Verify OSK is enabled in Windows Settings
3. Try running as Administrator (right-click → Run as administrator)
4. Contact your IT support if on a managed device