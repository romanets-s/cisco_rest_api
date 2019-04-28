
class Python:
	def load(self):
		return Game.load()

	def dump(self):
		return Game.dump()

	def get_random_movie(self):
		array = views.films
		for film in array:
			if not film.catch:
				return film

	def load_default_settings(self):
		return views.variables

	def get_strength(self):
		return views.player.power

	def get_movie(self, name):
		array = views.films
		for film in array:
			if film.title == name:
				return dict(film)
