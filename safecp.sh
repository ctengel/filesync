#!/bin/bash
SRC="$1"
TGT="$2"
TEM="$3"
FIL="$4"
cd "$SRC" || exit 1
sha1sum "$FIL" > "$FIL.sha1" || exit 1
cp "$FIL" "$TGT" || exit 1
sync || exit 1
sleep 5 || exit 1
sync || exit 1
echo "Verifying..." || exit 1
cp "$TGT/$FIL" "$TEM" || exit 1
cd "$TEM" || exit 1
cp "$SRC/$FIL.sha1" . || exit 1
sha1sum --check "$FIL.sha1" || exit 1
rm "$FIL" || exit 1
cd "$SRC" || exit 1
rm "$FIL" || exit 1
