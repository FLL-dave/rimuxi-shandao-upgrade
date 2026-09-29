# -*- coding: utf-8 -*-
import subprocess, json
cmd = ["lark-cli", "docs", "+fetch", "--doc", "Ms3XdtPKto1S1BxWJ7Vc45hynhd",
       "--scope", "section", "--start-block-id", "doxcnWjgtTvnDGorGHmVTVPvcnc", "--detail", "with-ids"]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("RC:", r.returncode)
print(r.stdout[:3000])
if r.stderr:
    print("ERR:", r.stderr[:500])
