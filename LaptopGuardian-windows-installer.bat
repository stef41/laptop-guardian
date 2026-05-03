@echo off
REM ============================================================
REM Laptop Guardian — Windows GUI Installer
REM Just double-click this file. Everything is automatic.
REM ============================================================
title Laptop Guardian Installer

REM Launch the PowerShell GUI installer
powershell -ExecutionPolicy Bypass -Command ^
  "& { ^
    Add-Type -AssemblyName System.Windows.Forms; ^
    Add-Type -AssemblyName System.Drawing; ^
    ^
    $form = New-Object System.Windows.Forms.Form; ^
    $form.Text = 'Laptop Guardian Installer'; ^
    $form.Size = New-Object System.Drawing.Size(500, 340); ^
    $form.StartPosition = 'CenterScreen'; ^
    $form.FormBorderStyle = 'FixedDialog'; ^
    $form.MaximizeBox = $false; ^
    $form.BackColor = [System.Drawing.Color]::FromArgb(15, 23, 42); ^
    $form.ForeColor = [System.Drawing.Color]::White; ^
    ^
    $title = New-Object System.Windows.Forms.Label; ^
    $title.Text = [char]::ConvertFromUtf32(0x1F6E1) + ' Laptop Guardian'; ^
    $title.Font = New-Object System.Drawing.Font('Segoe UI', 18, [System.Drawing.FontStyle]::Bold); ^
    $title.AutoSize = $true; ^
    $title.Location = New-Object System.Drawing.Point(30, 20); ^
    $title.ForeColor = [System.Drawing.Color]::White; ^
    $form.Controls.Add($title); ^
    ^
    $desc = New-Object System.Windows.Forms.Label; ^
    $desc.Text = 'Anti-theft protection for your laptop.`nLocks when your phone goes out of Bluetooth range.'; ^
    $desc.Font = New-Object System.Drawing.Font('Segoe UI', 10); ^
    $desc.Size = New-Object System.Drawing.Size(420, 50); ^
    $desc.Location = New-Object System.Drawing.Point(30, 65); ^
    $desc.ForeColor = [System.Drawing.Color]::FromArgb(148, 163, 184); ^
    $form.Controls.Add($desc); ^
    ^
    $progress = New-Object System.Windows.Forms.ProgressBar; ^
    $progress.Size = New-Object System.Drawing.Size(420, 24); ^
    $progress.Location = New-Object System.Drawing.Point(30, 140); ^
    $progress.Style = 'Continuous'; ^
    $form.Controls.Add($progress); ^
    ^
    $status = New-Object System.Windows.Forms.Label; ^
    $status.Text = 'Click Install to begin'; ^
    $status.Font = New-Object System.Drawing.Font('Segoe UI', 9); ^
    $status.Size = New-Object System.Drawing.Size(420, 25); ^
    $status.Location = New-Object System.Drawing.Point(30, 172); ^
    $status.ForeColor = [System.Drawing.Color]::FromArgb(148, 163, 184); ^
    $form.Controls.Add($status); ^
    ^
    $installBtn = New-Object System.Windows.Forms.Button; ^
    $installBtn.Text = 'Install'; ^
    $installBtn.Size = New-Object System.Drawing.Size(140, 44); ^
    $installBtn.Location = New-Object System.Drawing.Point(170, 220); ^
    $installBtn.FlatStyle = 'Flat'; ^
    $installBtn.BackColor = [System.Drawing.Color]::FromArgb(37, 99, 235); ^
    $installBtn.ForeColor = [System.Drawing.Color]::White; ^
    $installBtn.Font = New-Object System.Drawing.Font('Segoe UI', 11, [System.Drawing.FontStyle]::Bold); ^
    $installBtn.Cursor = [System.Windows.Forms.Cursors]::Hand; ^
    $form.Controls.Add($installBtn); ^
    ^
    $installBtn.Add_Click({ ^
      $installBtn.Enabled = $false; ^
      $installBtn.Text = 'Installing...'; ^
      $form.Refresh(); ^
      ^
      $installDir = \"$env:USERPROFILE\.laptop-guardian\"; ^
      ^
      $status.Text = 'Checking for Python...'; $progress.Value = 10; $form.Refresh(); ^
      $pyCmd = $null; ^
      try { $v = python --version 2>&1; if ($LASTEXITCODE -eq 0) { $pyCmd = 'python' } } catch {} ^
      if (-not $pyCmd) { try { $v = python3 --version 2>&1; if ($LASTEXITCODE -eq 0) { $pyCmd = 'python3' } } catch {} } ^
      ^
      if (-not $pyCmd) { ^
        $status.Text = 'Downloading Python...'; $progress.Value = 15; $form.Refresh(); ^
        $pyUrl = 'https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe'; ^
        $pyInstaller = \"$env:TEMP\python-installer.exe\"; ^
        (New-Object Net.WebClient).DownloadFile($pyUrl, $pyInstaller); ^
        ^
        $status.Text = 'Installing Python (this may take a minute)...'; $progress.Value = 25; $form.Refresh(); ^
        Start-Process -FilePath $pyInstaller -ArgumentList '/quiet', 'InstallAllUsers=0', 'PrependPath=1', 'Include_launcher=1' -Wait; ^
        ^
        $env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'Machine'); ^
        try { $v = python --version 2>&1; if ($LASTEXITCODE -eq 0) { $pyCmd = 'python' } } catch {} ^
        if (-not $pyCmd) { ^
          [System.Windows.Forms.MessageBox]::Show('Python installation failed. Please install Python from python.org and check Add to PATH.', 'Error', 'OK', 'Error'); ^
          $installBtn.Text = 'Install'; $installBtn.Enabled = $true; ^
          return; ^
        } ^
      } ^
      ^
      $status.Text = \"Found: $((& $pyCmd --version 2>&1))\"; $progress.Value = 35; $form.Refresh(); ^
      Start-Sleep -Seconds 1; ^
      ^
      if (Test-Path $installDir) { Remove-Item -Recurse -Force $installDir } ^
      ^
      $status.Text = 'Creating virtual environment...'; $progress.Value = 45; $form.Refresh(); ^
      & $pyCmd -m venv \"$installDir\venv\" 2>&1 | Out-Null; ^
      ^
      $status.Text = 'Installing Laptop Guardian...'; $progress.Value = 60; $form.Refresh(); ^
      & \"$installDir\venv\Scripts\pip.exe\" install --upgrade pip -q 2>&1 | Out-Null; ^
      $progress.Value = 70; $form.Refresh(); ^
      & \"$installDir\venv\Scripts\pip.exe\" install git+https://github.com/stef41/laptop-guardian.git -q 2>&1 | Out-Null; ^
      $progress.Value = 85; $form.Refresh(); ^
      ^
      $status.Text = 'Creating shortcuts...'; $progress.Value = 90; $form.Refresh(); ^
      ^
      $batContent = \"@echo off`r`ncall `\"$installDir\venv\Scripts\activate.bat`\"`r`nstart /b pythonw -m laptop_guardian.app\"; ^
      Set-Content -Path \"$installDir\laptop-guardian.bat\" -Value $batContent; ^
      ^
      $ws = New-Object -ComObject WScript.Shell; ^
      $desktop = $ws.CreateShortcut(\"$env:USERPROFILE\Desktop\Laptop Guardian.lnk\"); ^
      $desktop.TargetPath = \"$installDir\laptop-guardian.bat\"; ^
      $desktop.WorkingDirectory = $installDir; ^
      $desktop.Description = 'Anti-theft laptop protection'; ^
      $desktop.WindowStyle = 7; ^
      $desktop.Save(); ^
      ^
      $startMenu = \"$env:APPDATA\Microsoft\Windows\Start Menu\Programs\"; ^
      $sm = $ws.CreateShortcut(\"$startMenu\Laptop Guardian.lnk\"); ^
      $sm.TargetPath = \"$installDir\laptop-guardian.bat\"; ^
      $sm.WorkingDirectory = $installDir; ^
      $sm.Description = 'Anti-theft laptop protection'; ^
      $sm.WindowStyle = 7; ^
      $sm.Save(); ^
      ^
      $progress.Value = 100; ^
      $status.Text = 'Done! Laptop Guardian has been installed.'; ^
      $status.ForeColor = [System.Drawing.Color]::FromArgb(74, 222, 128); ^
      $installBtn.Text = 'Launch'; ^
      $installBtn.BackColor = [System.Drawing.Color]::FromArgb(22, 163, 74); ^
      $installBtn.Enabled = $true; ^
      ^
      $installBtn.remove_Click($installBtn.Tag); ^
      $installBtn.Tag = $installBtn.Add_Click({ ^
        Start-Process \"$installDir\laptop-guardian.bat\"; ^
        $form.Close(); ^
      }); ^
    }); ^
    ^
    $installBtn.Tag = $null; ^
    [void]$form.ShowDialog(); ^
  }"
