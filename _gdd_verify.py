# -*- coding: utf-8 -*-
import subprocess
cmd = ["lark-cli", "docs", "+fetch", "--doc", "Ms3XdtPKto1S1BxWJ7Vc45hynhd",
       "--scope", "section", "--start-block-id", "doxcnWjgtTvnDGorGHmVTVPvcnc", "--detail", "simple"]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[:2500])
