from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import models
from .forms import TaskForm, UpdateTaskForm, UpdateFertilizerForm, UpdateKandojobsForm, UpdateMilkForm
from .models import *


# Create your views here.


@never_cache
def Home(request):
    context = {
        "name": {"Home Farm Page"},
        'form': TaskForm
    }
    return render(request, 'mogoon/home.html', context)


@never_cache
def CropTable(request):
    data = Crop.objects.all()
    plucking_date = models.DateTimeField()
    crop_today = Crop.objects.count()
    crop_todate = Crop.objects.aggregate(all_sum=Sum('crop_today'))
    plucker_numbers = Crop.objects.aggregate(all_quantity=Sum('plucker_numbers'))
    plucking_average = F(crop_today) / F(plucker_numbers)
    total_crop = Crop.objects.aggregate(total_sum=Sum('crop_todate'))

    context = {

        "crop_data": data,
        "plucking_date": plucking_date,
        "c_today": crop_today,
        "c_todate": crop_todate,
        "p_numbers": plucker_numbers,
        "p_average": plucking_average,
        "t_crop": total_crop,

    }
    return render(request, 'mogoon/crop_table.html', context)


# raise Exception("I want to know value" + str("Crop Table"))


@never_cache
def CropTableUpdate(request):
    # get the current crop_todate value
    crop_todate = Crop.objects.aggregate(all_sum=Sum('crop_today'))

    # the crop_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is nul as shown below, when null is set to type None and not type
    # Null
    if crop_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        crop_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the crop_todate and pass it to the templates via the context, this value
        # appears in the form
        crop_todate = Crop.objects.aggregate(all_sum=Sum('crop_today'))
    context = {
        "crop_todate": crop_todate,

    }
    return render(request, 'mogoon/crop_table_update.html', context)


@never_cache
def mogoonCropCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The crop_todate is the crop todate gotten from the
        # form(that was passed from the notes function) plus the crop today entered in the form.
        # Initially the crop to date is zero when the dta base is empty. the new crop to date will be zero plus the crop
        # today entered in the form, this addition is inserted and saved in the database as crop todate as shown below.
        plucking_date = request.POST['plucking_date']
        crop_data = request.POST['crop_data']
        crop_today = request.POST['crop_today']
        # Initially request.POST['crop_today'] is a string, it has to be wrapped with an int for purpose of addition
        crop_todate = int(request.POST['crop_todate']) + int(crop_today)
        plucker_number = request.POST['plucker_number']
        plucking_average = request.POST['plucking_average']
        total_crop = request.POST['total_crop']

        insert = Crop(plucking_date=plucking_date, crop_data=crop_data, crop_today=crop_today, crop_todate=crop_todate,
                      plucker_numbers=plucker_number, plucking_average=plucking_average, total_crop=total_crop)
        insert.save()

    return redirect('/crop_table')


@never_cache
def KandojobsTable(request):
    data = Kandojobs.objects.all()
    pruning_done = models.DateTimeField()
    pruned_block_No = models.IntegerField()
    pruned_bushes = Kandojobs.objects.count()
    pruning_rate = models.DecimalField()
    pruning_cost = F(pruned_bushes) * F(pruning_rate)
    weeding_done = models.DateTimeField()
    chemical_name = models.CharField()
    block_No = models.IntegerField()
    cost_per_lit = models.DecimalField()
    weeding_chem_amt = models.DecimalField()
    weeding_labour_number = models.IntegerField()
    weeding_labour_rate = models.DecimalField()
    weeding_labour = F('weeding_labour_number') * F('weeding_labour_rate')
    weeding_cost = F('weeding_chem_amt') * F(cost_per_lit) + F(weeding_labour)

    context = {

        "kandojobs": data,
        "p_done": pruning_done,
        "p_b_No": pruned_block_No,
        "p_bushes": pruned_bushes,
        "pruning_rate": pruning_rate,
        "P_cost": pruning_cost,
        "w_done": weeding_done,
        "c_name": chemical_name,
        "b_No": block_No,
        "c_p_lit": cost_per_lit,
        "w_c_amt": weeding_chem_amt,
        "weeding_labour_number": weeding_labour_number,
        "weeding_labour_rate": weeding_labour_rate,
        "w_labour": weeding_labour,
        "w_cost": weeding_cost,
    }
    return render(request, 'mogoon/kandojobs_table.html', context)


@never_cache
def KandojobsTableUpdate(request):
    pruned_bushes = Kandojobs.objects.count()
    pruning_rate = models.DecimalField()
    pruning_cost = F(pruned_bushes) * F(pruning_rate)

    cost_per_lit = models.DecimalField()
    weeding_labour_number = models.IntegerField()
    weeding_labour_rate = models.DecimalField()
    weeding_chem_amt = models.DecimalField()
    weeding_labour = F(weeding_labour_number) * F(weeding_labour_rate)
    weeding_cost = F(weeding_chem_amt) * F(cost_per_lit) + F(weeding_labour)

    context = {
        "pruned_bushes": pruned_bushes,
        "pruning_rate": pruning_rate,
        "pruning_cost": pruning_cost,

        "cost_per_lit": cost_per_lit,
        "weeding_labour_number": weeding_labour_number,
        "weeding_labour_rate": weeding_labour_rate,
        "weeding_labour": weeding_labour,
        "weeding_chem_amt": weeding_chem_amt,
        "weeding_cost": weeding_cost,

    }
    return render(request, 'mogoon/kandojobs_table_update.html', context)


@never_cache
def mogoonKandojobsCreate(request):
    if request.method == "POST":
        pruning_done = request.POST['pruning_done']
        pruned_block_No = request.POST['pruned_block_No']
        pruned_bushes = request.POST['pruned_bushes']
        pruning_rate = request.POST['pruning_rate']
        pruning_cost = request.POST['pruning_cost']
        weeding_done = request.POST['weeding_done']
        chemical_name = request.POST['chemical_name']
        block_No = request.POST['block_No']
        cost_per_lit = request.POST['cost_per_lit']
        weeding_chem_amt = request.POST['weeding_chem_amt']
        weeding_labour_number = request.POST['weeding_labour_number']
        weeding_labour_rate = request.POST['weeding_labour_rate']
        weeding_labour = request.POST['weeding_labour']
        weeding_cost = request.POST['weeding_cost']

        insert = Kandojobs(pruned_block_No=pruned_block_No, pruned_bushes=pruned_bushes, pruning_done=pruning_done,
                           pruning_rate=pruning_rate, pruning_cost=pruning_cost, weeding_done=weeding_done,
                           chemical_name=chemical_name, block_No=block_No, cost_per_lit=cost_per_lit,
                           weeding_chem_amt=weeding_chem_amt, weeding_labour_number=weeding_labour_number,
                           weeding_labour_rate=weeding_labour_rate, weeding_labour=weeding_labour,
                           weeding_cost=weeding_cost)

        insert.save()
        return redirect('/kandojobs_table')


@never_cache
def MilkTable(request):
    data = Milk.objects.all()
    milking_done = models.DateTimeField()
    milk_today = Milk.objects.count()
    milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))
    cows_milked = Milk.objects.count()
    cow_numbers = Milk.objects.count()
    milking_average = F(milk_today) / F(cow_numbers)
    total_milk = Milk.objects.aggregate(total_sum=Sum('milk_todate'))
    calf_down = models.DateTimeField()
    calf_numbers = Milk.objects.count()
    vet_cost = models.FloatField()
    Total_vet_cost = Milk.objects.aggregate(total_cost=Sum('vet_cost'))

    context = {

        "Milk": data,
        "m_done": milking_done,
        "m_today": milk_today,
        "m_todate": milk_todate,
        "c_milked": cows_milked,
        "c_numbers": cow_numbers,
        "m_average": milking_average,
        "t_milk": total_milk,
        "cf_down": calf_down,
        "cf_numbers": calf_numbers,
        "v_cost": vet_cost,
        "T_v_cost": Total_vet_cost,
    }
    return render(request, 'mogoon/milk_table.html', context)


@never_cache
def MilkTableUpdate(request):
    # get the current milk_todate value
    milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))

    # the milk_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is nul as shown below, when null is set to type None and not type
    # Null
    if milk_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        milk_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the milk_todate and pass it to the templates via the context, this value
        # appears in the form
        milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))
    Total_vet_cost = Milk.objects.aggregate(total_cost=Sum('vet_cost'))
    context = {
        "milk_todate": milk_todate,
        "Total_vet_cost": Total_vet_cost,

    }
    return render(request, 'mogoon/milk_table_update.html', context)


@never_cache
def mogoonMilkCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The milk_todate is the Milk todate gotten from the
        # form(that was passed from the notes function) plus the Milk today entered in the form.
        # Initially the crop to date is zero when the dta base is empty. the new Milk to date will be zero plus the crop
        # today entered in the form, this addition is inserted and saved in the database as crop todate as shown below.
        milking_done = request.POST['milking_done']
        milk_today = request.POST['milk_today']
        milk_todate = int(request.POST['milk_todate']) + int(milk_today)
        # Initially request.POST['milk_today'] is a string, it has to be wrapped with an int for purpose of addition
        cows_milked = request.POST['cows_milked']
        cow_numbers = request.POST['cow_numbers']
        milking_average = request.POST['milking_average']
        total_milk = request.POST['total_milk']
        calf_down = request.POST['calf_down']
        calf_numbers = request.POST['calf_numbers']
        vet_cost = request.POST['vet_cost']
        Total_vet_cost = request.POST['Total_vet_cost']

        insert = Milk(milking_done=milking_done, milk_today=milk_today, milk_todate=milk_todate,
                      cows_milked=cows_milked,
                      cow_numbers=cow_numbers, milking_average=milking_average, total_milk=total_milk,
                      calf_down=calf_down, calf_numbers=calf_numbers, vet_cost=vet_cost, Total_vet_cost=Total_vet_cost)
        insert.save()
        return redirect('/milk_table')


@never_cache
def FertilizerTable(request):
    data = Fertilizer.objects.all()
    fertilizer_applied = models.DateTimeField()
    fertilizer_amt = Fertilizer.objects.count()
    fertilizer_labour_rate = models.DecimalField()
    fertilizer_labour = models.IntegerField()
    fertilizer_labour_cost = F(fertilizer_amt) * F(fertilizer_labour_rate)
    fertilizer_price = models.IntegerField()
    fertilizer_cost = F(fertilizer_amt) * F(fertilizer_price)
    fertilizer_total_cost = F(fertilizer_cost) + F(fertilizer_labour_cost)

    context = {

        "fertilizer": data,
        "f_applied": fertilizer_applied,
        "f_amt": fertilizer_amt,
        "f_l_rate": fertilizer_labour_rate,
        "f_labour": fertilizer_labour,
        "f_l_cost": fertilizer_labour_cost,
        "f_price": fertilizer_price,
        "f_cost": fertilizer_cost,
        "f_t_cost": fertilizer_total_cost,

    }
    return render(request, 'mogoon/fertilizer_table.html', context)


@never_cache
def mogoonFertilizerTableUpdate(request):
    fertilizer_amt = Fertilizer.objects.count()
    fertilizer_labour_rate = models.DecimalField()
    fertilizer_labour = models.IntegerField()
    fertilizer_labour_cost = F(fertilizer_amt) * F(fertilizer_labour_rate)
    fertilizer_price = models.DecimalField()
    fertilizer_cost = F(fertilizer_amt) * F(fertilizer_price)
    fertilizer_total_cost = F(fertilizer_cost) + F(fertilizer_labour_cost)
    context = {

        "fertilizer_amt": fertilizer_amt,
        "fertilizer_labour_rate": fertilizer_labour_rate,
        "fertilizer_labour": fertilizer_labour,
        "fertilizer_price": fertilizer_price,
        "fertilizer_labour_cost": fertilizer_labour_cost,
        "fertilizer_cost": fertilizer_cost,
        "fertilizer_total_cost": fertilizer_total_cost,

    }
    return render(request, 'mogoon/fertilizer_table_update.html', context)


@never_cache
def mogoonFertilizerCreate(request):
    if request.method == "POST":
        fertilizer = request.POST['fertilizer']
        fertilizer_applied = request.POST['fertilizer_applied']
        fertilizer_labour_rate = request.POST['fertilizer_labour_rate']
        fertilizer_amt = request.POST['fertilizer_amt']
        fertilizer_labour = request.POST['fertilizer_labour']
        fertilizer_labour_cost = request.POST['fertilizer_labour_cost']
        fertilizer_price = request.POST['fertilizer_price']
        fertilizer_cost = request.POST['fertilizer_cost']
        fertilizer_total_cost = request.POST['fertilizer_total_cost']

        insert = Fertilizer(fertilizer=fertilizer, fertilizer_applied=fertilizer_applied, fertilizer_amt=fertilizer_amt,
                            fertilizer_labour_rate=fertilizer_labour_rate,
                            fertilizer_labour=fertilizer_labour, fertilizer_labour_cost=fertilizer_labour_cost,
                            fertilizer_price=fertilizer_price,
                            fertilizer_cost=fertilizer_cost, fertilizer_total_cost=fertilizer_total_cost)
        insert.save()
        return redirect('/fertilizer_table')


# CRUD functionality for the tables
@never_cache
def update(request, pk):
    data = Crop.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/crop_table')

    else:
        form = UpdateTaskForm(instance=data)

    context = {
        'form': form, 'UpdateTaskForm': UpdateTaskForm,

    }
    return render(request, 'Crop_data/update.html', context)


@never_cache
def delete(request, pk):
    data = Crop.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/crop_table')

    context = {
        'item': data,
    }
    return render(request, 'Crop_data/delete.html', context)


@never_cache
def F_update(request, pk):
    data = Fertilizer.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateFertilizerForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/fertilizer_table')

    else:
        form = UpdateFertilizerForm(instance=data)

    context = {
        'form': form, 'UpdateFertilizerForm': UpdateFertilizerForm,

    }
    return render(request, 'Fertilizer/update.html', context)


@never_cache
def F_delete(request, pk):
    data = Fertilizer.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/fertilizer_table')

    context = {
        'item': data,
    }
    return render(request, 'Fertilizer/delete.html', context)


@never_cache
def K_update(request, pk):
    data = Kandojobs.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateKandojobsForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/kandojobs_table')

    else:
        form = UpdateKandojobsForm(instance=data)

    context = {
        'form': form, 'UpdateKandojobsForm': UpdateKandojobsForm,

    }
    return render(request, 'Kandojobs/update.html', context)


@never_cache
def K_delete(request, pk):
    data = Kandojobs.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/kandojobs_table')

    context = {
        'item': data,
    }
    return render(request, 'Kandojobs/delete.html', context)


@never_cache
def M_update(request, pk):
    data = Milk.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateMilkForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/milk_table')

    else:
        form = UpdateMilkForm(instance=data)

    context = {
        'form': form, 'UpdateMilkForm': UpdateMilkForm,

    }
    return render(request, 'Milk/update.html', context)


@never_cache
def M_delete(request, pk):
    data = Milk.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/milk_table')

    context = {
        'item': data,
    }
    return render(request, 'Milk/delete.html', context)
