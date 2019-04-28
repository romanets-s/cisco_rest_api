class Film:

	def __init__(self, json, id):
		self.id = id
		self.title = json['Title']
		self.poster = json['Poster']
		self.director = json['Director']
		self.year = json['Year']
		self.imdbRating = json['imdbRating']
		self.plot = json['Plot']
		self.actors = json['Actors']
		self.catch = False
