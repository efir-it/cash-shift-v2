from datetime import datetime
from typing import Optional, Dict
from fastapi import Depends, HTTPException, Request, status
import os
import sys

from config import settings

from os.path import abspath, dirname
