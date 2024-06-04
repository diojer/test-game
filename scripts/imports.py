from dataclasses import dataclass, field
import pygame, sys
from pygame import Vector2
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game
    from .entities import KinematicBody