import os
import secrets

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileAllowed, FileField, FileRequired
from processing import color_distribution, load_image, transform
from werkzeug.utils import secure_filename
from wtforms import SelectField, SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["RECAPTCHA_USE_SSL"] = False
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LdMBc0kAAAAAE9bSYQH3NKG92HEHaO3IF4mydhG"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LdMBc0kAAAAADShGxFuVyhqSjZyHKxozur3Mem6"
# app.config["SESSION_COOKIE_DOMAIN"] = False
app.config["RECAPTCHA_OPTIONS"] = {"theme": "dark light"}


bootstrap = Bootstrap(app)


class FormImage(FlaskForm):
    upload = FileField(
        "Загрузка изображения",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "png", "jpeg"], "Только изображения необходимо загружать!"
            ),
        ],
        description="jpg, png, jpeg",
        # render_kw={"class": "form-control", "type": "file"},
    )

    recaptcha = RecaptchaField()
    select_swap_method = SelectField(
        "Выберите метод обработки",
        choices=[
            ("0", "Горизонтальное разделение"),
            ("1", "Вертикальное разделение"),
        ],
    )
    submit = SubmitField("Обработать", render_kw={"class": "btn btn-success"})


@app.route("/", methods=["GET", "POST"])
def index():
    form = FormImage()
    original_image = None
    render_image = None
    color_image = None
    if request.method == "POST" and form.validate_on_submit():
        print("hi")
        original_image = os.path.join(
            "static", secure_filename(form.upload.data.filename)
        )
        print(original_image)
        form.upload.data.save(original_image)
        vertical = bool(int(form.select_swap_method.data))

        render, render_image = transform(load_image(original_image), vertical)
        if render is not None:
            _, color_image = color_distribution(render)
    else:
        print("Form is invalid")
        print(form.errors)
    return render_template(
        "index.html",
        form=form,
        original_image=original_image,
        render_image=render_image,
        color_image=color_image,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
