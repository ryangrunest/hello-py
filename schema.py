import graphene
import json
import uuid
from datetime import datetime


# to run, cd into folder, run pipenv shell, then command 'python schema.py'
class Post(graphene.ObjectType):
  title = graphene.String()
  content = graphene.String()

class User(graphene.ObjectType):
  id = graphene.ID(default_value=str(uuid.uuid4()))
  username = graphene.String(default_value="George")
  created_at = graphene.DateTime(default_value=(datetime.now()))
  avatar_url = graphene.String()

  def resolve_avatar_url(self, info):
    return 'https://cloudinary.com/{}/{}'.format(self.username, self.id)

class Query(graphene.ObjectType):
  # arguments for queries
  users = graphene.List(User, limit=graphene.Int())
  hello = graphene.String()
  is_admin = graphene.Boolean()

  def resolve_hello(self, info):
    return "world"

  def resolve_is_admin(self, info):
    return True

  def resolve_users(self, info, limit=None):
    return [
      User(username="Fred"),
      User(username="Ryan"),
      User(username="George")
    ][:limit]

class CreateUser(graphene.Mutation):
  user = graphene.Field(User)
  # arguments for mutations
  class Arguments:
    username = graphene.String()

  def mutate(self, info, username):
    user = User(username=username)
    return CreateUser(user=user)

class CreatePost(graphene.Mutation):
  # declare post field
  post = graphene.Field(Post)

  # arguments
  class Arguments:
    title = graphene.String()
    content = graphene.String()


  def mutate(self, info, title, content):
    if info.context.get('is_anonymous'):
      raise Exception('Not Authenticated!')
    post =  Post(title=title, content=content)
    return CreatePost(post=post)

class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
  '''
  {
    users {
      id
      createdAt
      username
      avatarUrl
    }
  }
  ''',
  context={ 'is_anonymous': True }
  # variable_values={ 'limit': 1 }
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))