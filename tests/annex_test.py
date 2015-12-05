import os
import uuid
import git
import annex.repo
from annex.key import Key

def test_repo(tmpdir):
	repo = annex.repo.Repo(tmpdir.dirname)
	repo.init()
	assert os.path.exists(os.path.join(tmpdir.dirname, '.git/annex'))

	cfg = repo.config_reader()
	assert 'annex' in repo.__repo_config__
	assert isinstance(repo.r_uuid, uuid.UUID)
	assert repo.r_version == 5

def test_keyname(tmpdir):
	key = Key()
	data = 'foobar'
	key.create(data)
	assert key.g_backend == 'sha256'.upper()
	assert key.g_name == 'c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'
	assert key.keyname() == 'SHA256-s6--c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'

def test_keypath():
	key = Key()
	keyname = 'SHA256-s6--c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'
	assert key.keypath(keyname) == '11d/8ca/'
