from filter_open_psychometrics_data_utils import preprocess_text

print(preprocess_text("dental science"))
print(preprocess_text("dentistry"))
print(preprocess_text("dentist"))

print(preprocess_text("chemical science"))
print(preprocess_text("chemistry"))

# historical
# psychological
# vet

print(preprocess_text("mathematical science"))
print(preprocess_text("mathematic"))
print(preprocess_text("mathematics"))
