#!/bin/bash

set -e

APP_NAME="sstrack"
APP_BUNDLE="dist/$APP_NAME.app"
ENTITLEMENTS_PATH="/Users/charlie/Desktop/SStrack/entitlements.plist"
SIGN_IDENTITY="Apple Distribution: GWAPP Technologies Inc."

echo "🔧 Setting environment to skip pkg_resources hook..."
export PYINSTALLER_NO_PKGRES=1

echo "🧼 Cleaning previous builds..."
rm -rf build dist __pycache__

echo "🚀 Building with PyInstaller..."
pyinstaller SStrack.spec

if [[ ! -f "$APP_BUNDLE/Contents/MacOS/$APP_NAME" ]]; then
    echo "❌ Build failed — binary not found. Exiting."
    exit 1
fi

echo "🔐 Signing the app bundle..."
codesign --deep --force --verify --verbose \
--entitlements "$ENTITLEMENTS_PATH" \
--options runtime \
--sign "$SIGN_IDENTITY" \
"$APP_BUNDLE"

echo "✅ Verifying signature..."
codesign --verify --deep --strict --verbose=2 "$APP_BUNDLE"

echo "🎉 Launching the app..."
open "$APP_BUNDLE"
