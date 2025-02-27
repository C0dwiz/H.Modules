# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# ---------------------------------------------------------------------------------
# Name: HModsLibrary
# Description: Library required for most H:Mods modules.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: HModsLibrary
# scope: HModsLibrary 0.0.1
# ---------------------------------------------------------------------------------

import logging
import re
from .. import loader, utils

logger = logging.getLogger(__name__)
__version__ = (0, 0, 1)

class HModsLib(loader.Library):
    """Library required for most H:Mods modules."""
    developer = "@hikka_mods"
    version = __version__
    
    async def parse_time(self, time_str):
        time_units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
        if not re.fullmatch(r'(\d+[dhms])+', time_str):
            return None
        seconds = 0
        matches = re.findall(r'(\d+)([dhms])', time_str)
        for amount, unit in matches:
            seconds += int(amount) * time_units[unit]
        return seconds if seconds > 0 else None
    
