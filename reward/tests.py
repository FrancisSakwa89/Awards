from django.test import TestCase
from .models import Profile, Project, Rating


# Create your tests here.
class ProfileTestClass(TestCase):
  """  
  Tests Profile class and its functions
  """
  def setUp(self):
    self.prof =Profile(profpic='test.jpg', bio='test bio', contact='hello@hello.com',user=1)

  def test_instance(self):
      self.assertTrue(isinstance(self.prof, Profile))

  def test_save_method(self):
      """
      Function to test that profile is being saved
      """
      self.prof.save_profile()
      profiles = Profile.objects.all()
      self.assertTrue(len(profiles) > 0)

  def test_delete_method(self):
      """
      Function to test that a profile can be deleted
      """
      self.prof.save_profile()
      self.prof.delete_profile()
      profiles = Profile.objects.all()
      self.assertTrue(len(profiles) == 0)



class ProjecTestClass(TestCase):
  """  
  Tests Project class and its functions
  """
  def setUp(self):
      self.project = Project(title='test title',image='test.jpg',description='test description',link='https://test.com',poster=1,postername='tester')

  def test_instance(self):
      self.assertTrue(isinstance(self.project, Project))

  def test_save_method(self):
      """
      Function to test that a project is being saved
      """
      self.project.save_project()
      projects = Project.objects.all()
      self.assertTrue(len(projects) > 0)

  def test_delete_method(self):
      """
      Function to test that a project can be deleted
      """
      self.project.save_project()
      self.project.delete_project()
      projects = Project.objects.all()
      self.assertTrue(len(projects) == 0)



class RatingTestClass(TestCase):
  """  
  Tests Rating Class and its functions
  """
  def setUp(self):
      self.project = Project(title='test title',image='test.jpg',description='test description',link='https://test.com',poster=1,postername='tester')
      self.rating = Rating(design=1,usability=1,content=1,average=1,project=1,postername='tester')

  def test_instance(self):
      self.assertTrue(isinstance(self.rating, Rating))

  def test_save_method(self):
      """
      Function to test that a rating is being saved
      """
      self.project.save_project()
      self.rating.save_rating()
      ratings = Rating.objects.all()
      self.assertTrue(len(ratings) > 0)

  def test_delete_method(self):
      """
      Function to test that a rating can be deleted
      """
      self.project.save_project()
      self.rating.save_rating()
      self.rating.delete_rating()
      ratings = Rating.objects.all()
      self.assertTrue(len(ratings) == 0)
