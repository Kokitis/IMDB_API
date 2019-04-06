import random
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ColorScheme:
	name: str
	palette: List[str]
	background: str
	ticks: str
	font: str

	def get_color(self, index: int) -> str:
		try:
			color = self.palette[index]
		except IndexError:
			color = _generate_random_color()
		return color


_colorschemes: List[ColorScheme] = [
	ColorScheme('graphtv',
		palette = [
			'#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
			'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
			'#79CEF2'
		],
		background = "#333333",
		ticks = "#999999",
		font = "#999999"

	)
]
colorschemes: Dict[str, ColorScheme] = {i.name: i for i in _colorschemes}


def _generate_random_color() -> str:
	lower = 100
	upper = 256
	red = random.randrange(lower, upper)
	blue = random.randrange(lower, upper)
	green = random.randrange(lower, upper)
	color = f'#{red:02X}{green:02X}{blue:02X}'
	return color


def get_colorscheme(key: str) -> ColorScheme:
	selected_colorscheme = colorschemes[key]
	return selected_colorscheme
