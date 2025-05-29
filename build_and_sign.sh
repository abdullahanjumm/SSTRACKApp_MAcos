#!/bin/bash

set -e

APP_NAME="sstrack"
APP_BUNDLE="dist/$APP_NAME.app"
ENTITLEMENTS_PATH="/Users/charlie/Desktop/SStrack/entitlements.plist"
SIGN_IDENTITY="3rd Party Mac Developer Application: GWAPP Technologies Inc."
PKG_SIGN_IDENTITY="3rd Party Mac Developer Installer: GWAPP Technologies Inc."
PKG_NAME="sstrack.pkg"

echo "🔧 Setting environment to skip pkg_resources hook..."
export PYINSTALLER_NO_PKGRES=1

echo "🧼 Cleaning previous builds..."
rm -rf build dist __pycache__ "$PKG_NAME"

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

echo "📦 Creating .pkg installer..."
productbuild \
--component "$APP_BUNDLE" /Applications \
--sign "$PKG_SIGN_IDENTITY" \
"$PKG_NAME"

echo "📦 Verifying .pkg..."
pkgutil --check-signature "$PKG_NAME"

echo "🎉 Build and signing completed. Ready to upload .pkg via Transporter."
