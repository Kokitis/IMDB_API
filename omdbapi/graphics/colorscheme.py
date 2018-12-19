from dataclasses import dataclass
import random
from typing import Tuple, List, Dict, Any


@dataclass
class Color:
	r: int
	g: int
	b: int

	@classmethod
	def random(cls, lower: int = 0, upper: int = 255) -> 'Color':
		red = random.randrange(lower, upper)
		blue = random.randrange(lower, upper)
		green = random.randrange(lower, upper)
		return cls(red, green, blue)

	@classmethod
	def from_rgb(cls, red: int, green: int, blue: int) -> 'Color':
		return cls(red, green, blue)

	@classmethod
	def from_hex(cls, string: str) -> 'Color':
		if string.startswith('#'):
			string = string[1:]
		red = int(string[:2], 16)
		green = int(string[2:4], 16)
		blue = int(string[4:6], 16)

		return cls(red, green, blue)

	@classmethod
	def parse(cls, *args):
		if len(args) == 1:
			values = args[0]
		else:
			values = args

		if isinstance(values, str):
			return cls.from_hex(values)
		else:
			return cls.from_rgb(*values)

	def to_hex(self) -> str:
		return '#{0:02X}{1:02X}{2:02X}'.format(self.r, self.g, self.b)

	def to_rgb(self) -> Tuple[int, int, int]:
		return self.r, self.g, self.b


@dataclass
class ColorScheme:
	name: str
	palette: List[Color]
	background: Color
	ticks: Color
	font: Color

	@classmethod
	def from_dict(cls, data:Dict[str,Any]):
		return cls(
			name = data['name'],
			palette = [Color.parse(i) for i in data['seasonColors']],
			background = Color.parse(data['backgroundColor']),
			ticks = Color.parse(data['ticksColor']),
			font = Color.parse(data['fontColor'])
		)

	def get_season_color(self, index:int)->Color:
		index -= 1
		try:
			color = self.palette[index]
		except IndexError:
			color = Color.random()
		return color


graphtv_scheme = {
	'name':       'graphtv',
	'seasonColors':    [
		'#79A6F2', '#79F292', '#EE7781', '#C9F279', '#F279ED',
		'#F9F2D4', '#F2B079', '#8D79F2', '#88F279', '#F279AB',
		'#79CEF2'
	],
	'backgroundColor': "#333333",
	'ticksColor':      "#999999",
	'fontColor':       "#999999"
}
GRAPHTV = ColorScheme.from_dict(graphtv_scheme)

if __name__ == '__main__':
	print(GRAPHTV)
