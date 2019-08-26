from backend.models import *

unit = 3

for i in range(3, 4):
    DcsTag.objects.bulk_create([
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS1X.REAL", satuan="um", left=800, top=470),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS1Y.REAL", satuan="um", left=800, top=490),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS2X.REAL", satuan="um", left=700, top=280),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS2Y.REAL", satuan="um", left=700, top=300),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS3X.REAL", satuan="um", left=570, top=280),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS3Y.REAL", satuan="um", left=570, top=300),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS4X.REAL", satuan="um", left=270, top=280),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAS4Y.REAL", satuan="um", left=270, top=300),
        DcsTag(AlatUnitDCS_id=str(i+3), tag=f"BLT{i}_BFPTAECC.REAL", satuan="um", left=840, top=380),
    ])



# for i in range(1, 7):
#     taga = 'BLT'+str(unit)+'_TURBV' + str(i) + '.REAL'
#     newTag = DcsTag(AlatUnitDCS_id=unit, tag=taga, satuan="um", left=0.1, top=0.1)
#     newTag.save()
#     for j in ['X', 'Y']:
#         tag = 'BLT'+str(unit)+'_TURSV' + str(i) + j + '.REAL'
#         newTag = DcsTag(AlatUnitDCS_id=unit,tag=tag,satuan="um",left=0.1,top=0.1)
#         newTag.save()
#
# for i in range(1,5):
#     for j in ['RT','LT']:
#         tagb = f"BLT{unit}_TURBBRG{i}{j}.REAL"
#         newTag = DcsTag(AlatUnitDCS_id=unit, tag=tagb, satuan="degC", left=0.1, top=0.1)
#         newTag.save()
#
# tagc = f"BLT{unit}_TURBECCENT.REAL"
# newTag = DcsTag(AlatUnitDCS_id=unit, tag=tagc, satuan="um", left=0.1, top=0.1)
# newTag.save()
#
# tagd = f"BLT{unit}_TURBAXDISPL1.REAL"
# newTag = DcsTag(AlatUnitDCS_id=unit, tag=tagd, satuan="mm", left=0.1, top=0.1)
# newTag.save()
#
# tage = f"BLT{unit}_TURBBRG5T.REAL"
# newTag = DcsTag(AlatUnitDCS_id=unit, tag=tage, satuan="degC", left=0.1, top=0.1)
# newTag.save()
#
# tagd = f"BLT{unit}_TURBBRG6T.REAL"
# newTag = DcsTag(AlatUnitDCS_id=unit, tag=tagd, satuan="degC", left=0.1, top=0.1)
# newTag.save()

