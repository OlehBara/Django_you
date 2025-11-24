import random
from django.shortcuts import redirect
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.urls import reverse


def guess_view(request):
    if request.GET.get("new"):
        request.session.pop("secret_number", None)
        request.session.pop("won", None)
        request.session["message"] = "Нове число загадано! Вгадай його"
        return redirect("guess")

    if request.method == "POST":
        guess_text = request.POST.get("guess", "").strip()

        if guess_text.isdigit():
            guess = int(guess_text)
            secret = request.session.get("secret_number")

            if guess == secret:
                request.session["message"] = "ВІТАЮ! Ти вгадав число!"
                request.session["won"] = True
            elif guess < secret:
                request.session["message"] = "Занадто мало! Спробуй більше."
            else:
                request.session["message"] = "Занадто багато! Спробуй менше."
        else:
            request.session["message"] = "Введи ціле число!"

        return redirect("guess") 

    message = request.session.pop("message", None)
    won = request.session.get("won", False)

    if "secret_number" not in request.session:
        request.session["secret_number"] = random.randint(1, 100)

    msg = f"<p><b>{message}</b></p>" if message else ""

    new_game_link = f'<p><a href="?new=1"><button>Спробувати ще раз</button></a></p>' if won else ""

    html = f"""
    <h2>Вгадай число від 1 до 100</h2>
    {msg}
    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
        <input type="number" name="guess" min="1" max="100" required>
        <button type="submit">Submit</button>
    </form>
    {new_game_link}
    """

    return HttpResponse(html)