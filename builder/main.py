# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Builder for native platform
"""

from SCons.Script import AlwaysBuild, Default, DefaultEnvironment

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

env = DefaultEnvironment()

config = configparser.ConfigParser()
config.read("platformio.ini")

try:
    gcc_version = config.get("env:" + env.get("PIOENV"), "custom_gcc_version")
except:
    gcc_version = ''

# Remove generic C/C++ tools
for k in ("CC", "CXX"):
    if k in env:
        del env[k]

# Preserve C and C++ build flags
backup_cflags = env.get("CFLAGS", [])
backup_cxxflags = env.get("CXXFLAGS", [])

# Scan for GCC compiler
env.Tool("gcc")
env.Tool("g++")

# Restore C/C++ build flags as they were overridden by env.Tool
env.Append(CFLAGS=backup_cflags, CXXFLAGS=backup_cxxflags)

if gcc_version.isnumeric():
    env.Replace(CC="gcc-" + gcc_version)
    env.Replace(CXX="g++-" + gcc_version)
    print("Using gcc-" + gcc_version + " as compiler.")

#
# Target: Build executable program
#

target_bin = env.BuildProgram()

#
# Target: Print binary size
#

target_size = env.Alias("size", target_bin, env.VerboseAction(
    "$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Default targets
#

Default([target_bin])
