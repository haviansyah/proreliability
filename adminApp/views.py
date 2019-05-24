from urllib.request import parse_keqv_list
from django.shortcuts import render
from django.http import HttpResponse
import json
import xlrd
import xlwt
import time
import datetime
from backend.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

def xls_to_response(xls, fname):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response

@api_view(['POST','GET'])
def api_download_unit_rekap(request):
    id_kondisi = request.GET.get("id_kondisi")
    id_unit = request.GET.get("id_unit")
    kondisi = Condition.objects.get(pk=id_kondisi)
    unit = Unit.objects.get(pk=id_unit)
    equipment = Equipment.objects.filter(Condition_id=id_kondisi, Unit_id=id_unit)
    reports = [get_report_equip(i) for i in equipment]
    name = unit.name
    book = xlwt.Workbook()
    judul = "DATA "+" "+kondisi.name+" "+name
    sheet1 = book.add_sheet(judul)
    row = sheet1.row(0)
    headfmt = xlwt.Style.easyxf("""
                font : bold on;  align: vert center, horiz center;
                pattern: pattern solid, fore_colour light_yellow; """)
    row.write(0,"No",headfmt)
    row.write(1,"Tanggal",headfmt)
    row.write(2,"Equipment",headfmt)
    row.write(3,"Nilai",headfmt)
    row.write(4,"Level",headfmt)
    row.write(5,"Titik Ukur",headfmt)
    row.write(6, "Analisa", headfmt)
    row.write(7, "Rekomenndasi", headfmt)
    row.write(8, "Catatan", headfmt)


    for key, report in enumerate(reports):
        row = sheet1.row(key+1)
        row.write(0,key+1)
        datefmt = xlwt.Style.easyxf(num_format_str='D-MMM-YY')
        row.write(1,report["tanggal"],datefmt)
        row.write(2,report["equipment_name"])
        row.write(3,report["nilai"])
        level = report["level"]
        equipment = Equipment.objects.get(pk=report["id"])
        detail = equipment.detail
        if detail is not None:
            row.write(6, detail.analisa)
            row.write(7, detail.rekomendasi)
            row.write(8, detail.catatan)
        else :
            row.write(6, "-")
            row.write(7, "-")
            row.write(8, "-")
        color = "white"
        cLevel = ""
        if level == 1 :
            cLevel = "A"
            color = "blue"
        elif level == 2 :
            cLevel = "B"
            color = "green"
        elif level == 3 :
            cLevel = "C"
            color = "yellow"
        else :
            cLevel = "D"
            color = "red"

        levelfmt = xlwt.Style.easyxf("pattern: pattern solid, fore_colour %s;" % color)
        row.write(4,cLevel,levelfmt)
        row.write(5,report["titik_ukur"])


    return xls_to_response(book,judul+".xls")


@api_view(['POST','GET'])
def api_get_detail_equipment(request):
    if request.method == 'GET':
        id_equipment = request.GET.get("id")
        equipment = Equipment.objects.get(pk=id_equipment)
        detail = equipment.detail
        if detail is not None:
            data = {
                "analisa": detail.analisa,
                "rekomendasi": detail.rekomendasi,
                "catatan": detail.catatan
            }
        else :
            data = {

                "analisa": None,
                "rekomendasi": None,
                "catatan": None
            }
        return Response({"id": equipment.id, "name": equipment.name, "detail": data})
    elif request.method == 'POST':
        id_equipment = request.POST["id"]
        analisa = request.POST.get("analisa",None)
        rekomendasi = request.POST.get("rekomendasi", None)
        catatan = request.POST.get("catatan", None)
        newDetail = EqDetail(Equipment_id=id_equipment, analisa=analisa, rekomendasi=rekomendasi, catatan=catatan)
        newDetail.save()
        return Response({"status": "success"})


@api_view(['POST'])
def api_get_condition(request):
    id_kondisi = request.POST["id"]
    kondisi = Condition.objects.get(pk=id_kondisi)
    unit = kondisi.Unit.all()
    data = [{"id":i.id,"name": i.name, "count_level": get_count_level([get_report_equip(i) for i in Equipment.objects.filter(Condition_id=id_kondisi, Unit_id=i.id)])}for i in unit]
    name = kondisi.name
    return Response({"id":kondisi.id,"name":name,"units":data})


@api_view(['POST'])
def api_get_unit(request):
    id_kondisi = request.POST["kondisi_id"]
    id_unit = request.POST["unit_id"]
    level = int(request.POST.get('level', 0))
    unit = Unit.objects.get(pk=id_unit)
    equipment = Equipment.objects.filter(Condition_id=id_kondisi, Unit_id=id_unit)
    report = [get_report_equip(i) for i in equipment]
    if level != 0:
        report = list(filter(lambda x: x["level"] == level, report))
    name = unit.name
    count_level = get_count_level(report)
    hasil = {
        "name" : name,
        "report" : report,
        "count_level" : count_level
    }
    return Response(hasil)


def get_report_equip(equipment):
    latest = equipment.monitoringrow_set.latest('tanggal')
    monitoringSet = latest.monitoringdata_set.all()
    monitoringSet = list(filter(lambda x:x.Header.hitung == True,monitoringSet))
    MonDataMod = [[i.id, i.level,i.nilai] for i in monitoringSet]
    maks_level = max(MonDataMod, key=lambda x: x[1])
    maks_cal_nilai = filter(lambda x : x[1] == maks_level[1],MonDataMod)
    maks = max(maks_cal_nilai, key = lambda x:x[2])
    maks_data = MonitoringData.objects.get(pk=maks[0])
    ret = {}
    ret["id"] = equipment.id
    ret["tanggal"] = latest.tanggal
    ret["equipment_name"] = equipment.name
    ret["nilai"] = maks_data.nilai
    ret["level"] = maks_data.level
    ret["titik_ukur"] = maks_data.Header.name
    ret["hitung"] = maks_data.Header.hitung
    return ret


def get_count_level(unit):
    normal = len(list(filter(lambda d: d["level"] == 1 or d["level"] == 2,unit)))
    warning = len(list(filter(lambda d: d["level"] == 3,unit)))
    danger = len(list(filter(lambda d: d["level"] == 4,unit)))
    return {"normal":normal,"warning":warning,"danger":danger}


@api_view(['POST'])
def api_get_laporan(request):
    id_kondisi = request.POST["kondisi"]
    id_unit = request.POST["unit"]
    equipment = Equipment.objects.filter(Condition_id=id_kondisi, Unit_id=id_unit)
    report = [get_report_equip(i) for i in equipment]
    return Response(report)


@api_view(['POST'])
def api_get_equipment(request):
    id_equipment = request.POST["id"]
    equipment = Equipment.objects.get(pk=id_equipment)
    name = equipment.name
    header = [{"id":i.id,"name":i.name} for i in equipment.header_set.all()]
    hasil = {"name":name,"headers":header}
    return Response(hasil)


@api_view(['POST'])
def api_get_trend(request):
    id_equipment = request.POST["id"]
    equipment = Equipment.objects.get(pk=id_equipment)
    header = [{"id": i.id, "name": i.name, "dataset": get_data_header(i)} for i in equipment.header_set.all()]
    hasil = {"name": equipment.name, "data": header}
    return Response(hasil)


def get_data_header(header):
    data = [[i.MonitoringRow.tanggal,  i.nilai] for i in header.monitoringdata_set.order_by('MonitoringRow__tanggal')]
    return data


@api_view(['POST'])
def api_get_header(request):
    id_header = request.POST["id"]
    header = Header.objects.get(pk=id_header)
    name = header.name
    data = [{"tanggal":i.MonitoringRow.tanggal,"nilai":i.nilai} for i in header.monitoringdata_set.order_by('MonitoringRow__tanggal')]
    hasil = {"name":name, "data":data}
    return Response(hasil)


def get_header(sheet):
    ret = []
    for k,cell in enumerate(sheet.row(1)):
        stand = sheet.col_values(k,sheet.nrows-3)
        ret.append([cell.value, stand])
    return ret


def index(request):
    return render(request,'adminApp/index.html')


def get_report(request):
    id_kondisi = request.POST["kondisi"]
    id_unit = request.POST["unit"]
    equipment = Equipment.objects.filter(Condition_id=id_kondisi,Unit_id=id_unit)
    report = [get_report_equip(i) for i in equipment]
    hasil = json.dumps(report,indent=4, sort_keys=True, default=str)
    return HttpResponse(hasil,content_type="application/json")


def testing(request):
    eqt = Equipment.objects.get(pk=1)
    newMRow = MonitoringRow(tanggal='2017-06-20', waktu='09:00:00', Equipment = eqt)
    querySet = Equipment.objects.get(pk=1).monitoringrow_set.filter(tanggal='2017-06-20', waktu='09:00:00', Equipment = eqt).count()
    return HttpResponse(querySet)
    # if newMRow in querySet:
    #     return HttpResponse(newMRow.__dict__)
    # else:
    #     return HttpResponse(newMRow)


@api_view(['POST'])
def insert(request):
    start = time.time()
    data = request.FILES.get('data')
    kondisi_name = request.POST['kondisi']
    unit_name = request.POST['unit']

    if Unit.objects.filter(name=unit_name).count() == 0 :
        newUnit = Unit(name=request.POST["unit"])
        newUnit.save()
    else:
        newUnit = Unit.objects.filter(name = unit_name).first()

    if Condition.objects.filter(name=kondisi_name).count() == 0 :
        newCondition = Condition(name=request.POST['kondisi'])
        newCondition.save()
        newCondition.Unit.add(newUnit)
    else:
        newCondition = Condition.objects.get(name = kondisi_name)
        if not newCondition.Unit.filter(pk=newUnit.id) :
            newCondition.Unit.add(newUnit)
    book = xlrd.open_workbook(data.name, file_contents=data.read())
    error = []
    for sheet in book.sheets():
        adaEq = False
        equipment_name = sheet.cell_value(rowx=0, colx=0)
        if Equipment.objects.filter(name=equipment_name,Condition_id=newCondition.id,Unit_id=newUnit.id).count() == 0:
            newEq = Equipment(name=equipment_name,Unit=newUnit,Condition=newCondition)
            newEq.save()
        else:
            newEq = Equipment.objects.get(name=equipment_name, Unit=newUnit,Condition=newCondition)
            adaEq = True
        equipment_id = newEq.id
        header_ids = []

        # INSERTING HEADER & STANDARD

        if not adaEq:
            for headers in get_header(sheet)[3:-1]:
                hit = True
                if headers[0].strip().lower() is "fan" :
                    hit = False
                newHeader = Header(Equipment=newEq,name=headers[0],hitung=hit)
                newHeader.save()
                header_id = newHeader.id

                # INSERTING STANDARD
                b_normal  = headers[1][0] or 0.0
                b_warning = headers[1][1] or 0.0
                b_danger= headers[1][2] or 0.0

                newStd = Standard(Header=newHeader, batas_normal=b_normal, batas_warning=b_warning, batas_danger=b_danger)
                newStd.save()

                header_ids.append(header_id)
        else:
            header_ids = [i.id for i in newEq.header_set.order_by('pk')]
        # INSERTING ROW DATA

        for row in range(2, sheet.nrows - 3):
            if sheet.cell_value(row, 1) != '':
                tanggal_type = sheet.cell_type(row, 1)
                if tanggal_type != 3 :
                    error.append({
                        "equipment" : newEq.name,
                        "baris" : row+1,
                        "kolom": "tanggal"
                    })
                    continue

                tanggal = sheet.cell_value(row, 1)
                tanggal_datetime = datetime.datetime(*xlrd.xldate_as_tuple(tanggal, book.datemode))
                tanggal_string = tanggal_datetime.strftime("%Y-%m-%d")
                waktu = sheet.cell_value(row, 2)
                waktu_type = sheet.cell_type(row,2)
                waktu_string = None

                if waktu != '' and waktu_type == 3 :
                    waktu_2 = int(waktu * 24 * 3600)  # convert to number of seconds
                    try :
                        waktu_time = datetime.time(int(waktu_2 // 3600), int((waktu_2 % 3600) // 60), int(waktu_2 % 60))
                        waktu_string = waktu_time.strftime("%H:%M:%S")
                    except :
                        error.append({
                            "equipment": newEq.name,
                            "baris": row+1,
                            "kolom" : "waktu"
                        })


                if newEq.monitoringrow_set.filter(tanggal=tanggal_string,waktu=waktu_string,Equipment=newEq).exists():
                    continue
                newMRow = MonitoringRow(tanggal=tanggal_string, waktu=waktu_string,Equipment=newEq)
                newMRow.save()
                id_monitor_row = newMRow.id
                # INSERT DATA ALL
                newMDatas = []
                for col in range(3, sheet.ncols - 1):
                    header_idx = col - 3
                    nilai = sheet.cell_value(row, col)
                    tipe = sheet.cell_type(row, col)
                    if tipe == 2:
                        newMData = MonitoringData(MonitoringRow=newMRow,nilai=nilai,Header_id=header_ids[header_idx])
                        newMDatas.append(newMData)
                MonitoringData.objects.bulk_create(newMDatas)
                if len(newMRow.monitoringdata_set.all()) == 0 :
                    newMRow.delete()
    end = time.time()

    if len(error) != 0 :
        ret = {
            "status" : "error",
            "details" : error,
            "runtime": end - start,
        }
    else :
        ret = {
            "status": "success",
            "runtime": end - start,
        }

    return Response(ret)
