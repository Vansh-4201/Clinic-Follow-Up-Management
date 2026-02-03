from django.shortcuts import render

# Create your views here.

from django.core.paginator import Paginator


from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from .models import FollowUp, PublicViewLog
from .forms import FollowUpForm



import csv
from django.http import HttpResponse



@login_required
def dashboard(request):
    user = request.user
    clinic = user.userprofile.clinic

    followups = FollowUp.objects.filter(clinic=clinic)

    # Filters
    status = request.GET.get("status")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if status:
        followups = followups.filter(status=status)

    if start_date:
        followups = followups.filter(due_date__gte=start_date)

    if end_date:
        followups = followups.filter(due_date__lte=end_date)

    # Summary counts
    total_count = FollowUp.objects.filter(clinic=clinic).count()
    pending_count = FollowUp.objects.filter(clinic=clinic, status="pending").count()
    done_count = FollowUp.objects.filter(clinic=clinic, status="done").count()

    # View counts
    followups = followups.annotate(view_count=Count("publicviewlog"))

    context = {
        "followups": followups,
        "total_count": total_count,
        "pending_count": pending_count,
        "done_count": done_count,
    }

    return render(request, "dashboard.html", context)

@login_required
def create_followup(request):
    clinic = request.user.userprofile.clinic

    if request.method == "POST":
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.clinic = clinic
            followup.created_by = request.user
            followup.save()
            messages.success(request, "Follow-up created successfully.")
            return redirect("dashboard")
    else:
        form = FollowUpForm()

    return render(request, "followup_form.html", {"form": form})


@login_required
def edit_followup(request, pk):
    clinic = request.user.userprofile.clinic

    followup = get_object_or_404(
        FollowUp,
        pk=pk,
        clinic=clinic,   # 🔐 authorization enforced here
    )

    if request.method == "POST":
        form = FollowUpForm(request.POST, instance=followup)
        if form.is_valid():
            form.save()
            messages.success(request, "Follow-up updated successfully.")
            return redirect("dashboard")
    else:
        form = FollowUpForm(instance=followup)

    return render(request, "followup_form.html", {"form": form})



@login_required
def mark_followup_done(request, pk):
    if request.method != "POST":
        return redirect("dashboard")

    clinic = request.user.userprofile.clinic

    followup = get_object_or_404(
        FollowUp,
        pk=pk,
        clinic=clinic,   # 🔐 authorization enforced
    )

    followup.status = "done"
    followup.save()

    messages.success(request, "Follow-up marked as done.")
    return redirect("dashboard")



def public_followup(request, token):
    followup = get_object_or_404(FollowUp, public_token=token)

    # Log the view
    PublicViewLog.objects.create(
        followup=followup,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    # Language-based instruction
    if followup.language == "hi":
        message = "कृपया अपनी निर्धारित फॉलो-अप के लिए क्लिनिक से संपर्क करें।"
    else:
        message = "Please contact the clinic for your scheduled follow-up."

    return render(
        request,
        "public_followup.html",
        {
            "followup": followup,
            "message": message,
        },
    )


@login_required
def delete_followup(request, pk):
    if request.method != "POST":
        return redirect("dashboard")

    clinic = request.user.userprofile.clinic

    followup = get_object_or_404(
        FollowUp,
        pk=pk,
        clinic=clinic,   # 🔐 authorization enforced
    )

    followup.delete()
    messages.success(request, "Follow-up deleted successfully.")

    return redirect("dashboard")



@login_required
def export_followups_csv(request):
    clinic = request.user.userprofile.clinic

    followups = FollowUp.objects.filter(clinic=clinic).order_by("-created_at")

    response = HttpResponse(
        content_type="text/csv"
    )
    response["Content-Disposition"] = 'attachment; filename="followups.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Patient Name",
        "Phone",
        "Language",
        "Due Date",
        "Status",
        "Created At",
    ])

    for f in followups:
        writer.writerow([
            f.patient_name,
            f.phone,
            f.language,
            f.due_date,
            f.status,
            f.created_at,
        ])

    return response
