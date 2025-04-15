from library_app import db
from library_app.models import User, Book

# db.drop_all()
db.create_all()

users = []

users[0] = User(email="admin_user@test.com", username="admin_user", password="123", student=False, administrator=True, librarian=False)
db.session.add(users[0])

for _ in range(1, 101):
    users[_] = User(email=f"test_user{_}@test.com", username=f"test_user{_}", password="123", student=True, administrator=False, librarian=False)
    db.session.add(users[_])

for _ in range(101, 104):
    users[_] = User(email=f"librarian_user{_}@test.com", username=f"librarian_user{_}", password="123", student=False, administrator=False, librarian=True)
    db.session.add(users[_])

books = []

# todo: ダミーデータを生成するライブラリか何かを用いる

for _ in range(0, 101):
    books[_] = Book(title=f"テスト書名{_}", author=f"テスト著者名{_}")
    db.session.add(books[_])

db.session.commit()
