#run in shell to populate database with seed data
#run python manage.py shell
#copy and paste script
#exec(script)
script = """
from snippets.models import Snippet


def populate_db():
 snippet1 = Snippet(language= 'Python', code = 'print("Hello, World!")')
 snippet1.save()
  
snippet2 = Snippet(language= 'Python', code = 'def add(a, b):return a + b')
snippet2.save()

snippet3 = Snippet(language= 'Python', code = 'class Circle:def __init__(self, radius):self.radius = radius def area(self):return 3.14 * self.radius ** 2')
snippet3.save()
    
snippet4 = Snippet(language= 'JavaScript', code =  'console.log("Hello, World!");')
snippet4.save()

snippet5 = Snippet(language= 'Java', code =  'public class HelloWorld {public static void main(String[] args) {System.out.println("Hello, World!");}}')
snippet5.save()
"""
