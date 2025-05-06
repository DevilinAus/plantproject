def add_n(n):
    def add_x(b):
        return b + n

    return add_x


b = 10

add_4 = add_n(4)
add_5 = add_n(5)

print(add_5(10))


# demo of whats happening with the functional / wraping, see admin.py for squished version.
def secure_route():
    if "email" in session:
        return watering()
    else:
        return flask.redirect(flask.url_for("auth.login"))


def watering():
    return render_template("watering.html")


# more complete version of the above.


def login_required(route):
    def secure_route():
        if "email" in session:
            return route()
        else:
            return flask.redirect(flask.url_for("auth.login"))

    return secure_route
