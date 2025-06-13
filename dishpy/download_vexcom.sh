#!/bin/bash
echo "⬇️ Downloading VEX extension bundle..."
curl -L --progress-bar https://openvsxorg.blob.core.windows.net/resources/VEXRobotics/vexcode/0.6.1/VEXRobotics.vexcode-0.6.1.vsix -o vexcode.vsix
echo "📦 Extracting extension files..."
unzip -q vexcode.vsix #&& rm vexcode.vsix
echo "📂 Copying VEXcom tools..."
mkdir vexcom
# there is a .../tools/vexcom/{osx,win32,etc.}/vexcom
mv extension/resources/tools/vexcom/* ./vexcom
rm "[Content_Types].xml" extension.vsixmanifest
rm -rf extension
