from django.shortcuts import render
import random
import string

def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def captcha_view(request):
    if 'captcha' not in request.session:
        request.session['captcha'] = generate_captcha()
        request.session['attempts'] = 0

    message = ""
    disabled = False

    if request.method == "POST":
        user_input = request.POST.get("captcha")

        if user_input == request.session['captcha']:
            message = "Captcha matched successfully"
            request.session['attempts'] = 0
            request.session['captcha'] = generate_captcha()
        else:
            request.session['attempts'] += 1
            if request.session['attempts'] >= 3:
                disabled = True
                message = "Too many wrong attempts. Textbox disabled."
            else:
                message = "Captcha mismatch"
                request.session['captcha'] = generate_captcha()

    return render(request, "captcha_app/captcha.html", {
        "captcha": request.session['captcha'],
        "message": message,
        "disabled": disabled
    })
