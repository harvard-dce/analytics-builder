
from invoke import task
from os import getenv as env
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), '.env'))

AWS_PROFILE = env('AWS_PROFILE')
STACK_TAGS = env('STACK_TAGS')
STACK_NAME = env('STACK_NAME', 'analytics-builder')
GITHUB_OAUTH_TOKEN = env('GITHUB_OAUTH_TOKEN')

def profile_arg():
    if AWS_PROFILE is not None:
        return "--profile {}".format(AWS_PROFILE)
    return ""

def stack_tags():
    if STACK_TAGS is not None:
        return "--tags {}".format(STACK_TAGS)
    return ""


@task
def create(ctx):
    __create_or_update(ctx, "create")


@task
def update(ctx):
    __create_or_update(ctx, "update")


@task
def delete(ctx):

    cmd = ("aws {} cloudformation delete-stack "
           "--stack-name {}").format(profile_arg(), STACK_NAME)
    if input('are you sure? [y/N] ').lower().strip().startswith('y'):
        ctx.run(cmd)
    else:
        print("not deleting stack")


def __create_or_update(ctx, op):
    template_path = join(dirname(__file__), 'template.yml')

    cmd = ("aws {} cloudformation {}-stack {} "
           "--capabilities CAPABILITY_NAMED_IAM --stack-name {} "
           "--template-body file://{} "
           "--parameters "
           "ParameterKey=GithubOAuthToken,ParameterValue={} ")\
            .format(
                profile_arg(),
                op,
                stack_tags(),
                STACK_NAME,
                template_path,
                GITHUB_OAUTH_TOKEN
            )
    print(cmd)
#    ctx.run(cmd)

