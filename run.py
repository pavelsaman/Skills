from skills.models import Skill, Category, User
from skills import create_app, db


app = create_app(debug=True)
app.run(debug=True)


@app.shell_context_processor  # it will be registered with flask shell
def make_shell_context():
    return {'db': db, 'Skill': Skill, 'Category': Category, 'User': User}
