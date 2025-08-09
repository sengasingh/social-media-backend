from sqlalchemy import create_engine, ForeignKey, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class users(Base):
    __tablename__ = "users"
    userID = Column("userID", String, primary_key=True, default=generate_uuid)
    firstName = Column("firstName", String)
    lastName = Column("lastName", String)
    profileName = Column("profileName", String)
    email = Column("email", String)

    def __init__(self, firstName, lastName, profileName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.profileName = profileName
        self.email = email

class posts(Base):
    __tablename__ = "posts"
    postID = Column("postID", String, primary_key=True, default=generate_uuid)
    userID = Column("userID", String, ForeignKey("users.userID"))
    postContent = Column("postContent", String)

    def __init__(self, userID, postContent):
        self.userID = userID
        self.postContent = postContent

class likes(Base):
    __tablename__ = "likes"
    likeID = Column("likeID", String, primary_key=True, default=generate_uuid)
    userID = Column("userID", String, ForeignKey("users.userID"))
    postID = Column("postID", String, ForeignKey("posts.postID"))

    def __init__(self, userID, postID):
        self.userID = userID
        self.postID = postID

def addUser(firstName, lastName, profileName, email, session):
    exist = session.query(users).filter(users.email==email).all()
    if len(exist) > 0:
        print("user already exists")
    else:
        user = users(firstName, lastName, profileName, email)
        session.add(user)
        session.commit()
        print("user added to db")

def addPost(userID, postContent, session):
    newPost = posts(userID, postContent)
    session.add(newPost)
    session.commit()

def addLike(userID, postID, session):
    like = likes(userID, postID)
    session.add(like)
    session.commit()
    print("like was added")

db = "sqlite:///socialDB.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create User
'''
firstName = "Senga"
lastName = "Singh"
profileName = "SS0611"
email = "senga@gmail.com"

user = users(firstName, lastName, profileName, email)
session.add(user)
session.commit()
print("user added to db")
'''

#Create Post
'''
userID = "da711394-a9ca-4880-bb8d-661faf18d92a"
postContent = "Who tryna hang?"
newPost = posts(userID, postContent)
session.add(newPost)
session.commit()
'''

#addUser("Hog", "Rider", "HR0101", "hooooogridaaaa@gmail.com", session)
#addPost("3990eeac-376f-4d93-9969-dc58e7d36e21", "FAANG ain't ready!", session)
#addLike("da711394-a9ca-4880-bb8d-661faf18d92a", "bb872304-4d11-453c-b6f7-373b1657634f", session)

# Get All User's Posts By First Name
'''
userfname = "Needa"
user = session.query(users).filter(users.firstName == userfname).one_or_none()
if user is None:
    raise ValueError("user not found")
allposts = session.query(posts).filter(posts.userID == user.userID).all()
postsFilteredByUser = [p.postContent for p in allposts]
print(postsFilteredByUser)
'''

# Get All User's Posts By ID (received with request)
'''
userID = "da711394-a9ca-4880-bb8d-661faf18d92a"
allPosts = session.query(posts).filter(posts.userID == userID).all()
postsFilteredByUser = [p.postContent for p in allPosts]
print(postsFilteredByUser)
'''

# Get Like Count By Post ID (like button stores postID)
'''
post_id = "bb872304-4d11-453c-b6f7-373b1657634f"
getPostLikes = session.query(likes).filter(posts.postID==post_id).all()
print(len(getPostLikes))
'''

# INNER JOIN query (connects users & likes based on userID)
post_id = "bb872304-4d11-453c-b6f7-373b1657634f"
usersLikedPost = session.query(users, likes).filter(likes.postID == post_id).filter(likes.userID == users.userID).all()
for user_obj, like_obj in usersLikedPost:
    # Prints users' full names that liked post
    print(user_obj.firstName, user_obj.lastName)

#test
print("test")
