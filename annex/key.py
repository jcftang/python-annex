import hashlib

class Key(object):
	__struct__ = dict(
				g_backend='',
				g_size='s',
				g_modified='m',
				g_chunk_size='S',
				g_chunk_no='C',
				g_name='',
				g_ext='',
			)
	__order__ = ['g_backend', 'g_size', 'g_modified', 'g_chunk_size', 'g_chunk_no']

	def __init__(self):
		self.g_backend = None
		self.g_size = None
		self.g_modified = None
		self.g_chunk_size = None
		self.g_chunk_no = None
		self.g_name = None
		self.g_ext = None

	def create(self, data=None, backend='sha256', chunk=False):
		self.g_size = len(data)
		self.g_backend = backend.upper()
		h = hashlib.new(backend.lower())
		h.update(data)
		self.g_name = h.hexdigest()

	def keyname(self):
		parts = []

		for k in self.__order__:
			if getattr(self, k) is not None:
				parts.append("{0}{1}".format(self.__struct__[k], getattr(self, k)))

		part1 = '-'.join(parts)
		
		keyparts = []
		keyparts.append(part1)

		names = ['g_name','g_ext']
		parts = []
		for k in names:
			if getattr(self, k) is not None:
				parts.append("{0}{1}".format(self.__struct__[k], getattr(self, k)))
		part2 = '-'.join(parts)
		keyparts.append(part2)

		return '--'.join(keyparts)

	def keypath(self, key):
		h = hashlib.new('md5')
		h.update(key)
		digest = h.hexdigest()
		return "%s/%s/" % (digest[:3], digest[3:6])
