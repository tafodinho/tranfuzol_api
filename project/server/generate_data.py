from faker import Faker
import random
from project.server.models.Donor import Donor
from project.server.models.Subscriber import Subscriber
from project.server.models.Hospital import Hospital
from project.server.models.Transfusion import Transfusion
from project.server.models.Donation import Donation
from project.server.models.Deferral import Deferral
from project.server import db

fake = Faker()
blood_groups = ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+']
rhesus_factor =['D+', 'D-']
gender = ['make', 'female']

medicalConditions = [
    "Hypertnesion",
    "Diabeted",
    "HIV/AIDS",
    "Sickle Cell",
    "Chronic Kidnew Disease",
    "Cancer",
    "others"
]

bloodTypes = [
    "Whole blood",
    "Packed red cell",
    "Platelet concentrate",
    "Fresh frozon plasma"
]

hospitalUnits = [
    "Medicine",
    "Surgery", 
    "Obsterics/Gynaecology",
    "Maternity",
    "Pediatrics",
    "TB"
]

def donor(ref_id, hosp_id):
    donor = Donor()
    donor.sn = fake.ssn()
    donor.email = fake.email()
    donor.hospital_id = hosp_id
    donor.first_name = fake.first_name()
    donor.middle_name = fake.last_name()
    donor.last_name = fake.first_name_female()
    donor.home_address = fake.address()
    donor.city = fake.city()
    donor.region = fake.city()
    donor.phone1 = fake.phone_number()
    donor.phone2 = fake.phone_number()
    donor.cni = fake.isbn13()
    donor.cni_doi = fake.date_time()
    donor.cni_poi = fake.city()
    donor.dob = fake.date_time()
    donor.pob = fake.city()
    donor.gender = random.choice(gender)
    donor.blood_group = random.choice(blood_groups)
    donor.referrer_id = ref_id
    
    donor.allergies = fake.sentence(nb_words=4, variable_nb_words=True)
    donor.rhesus_factor = random.choice(rhesus_factor)
    donor.medical_conditions = fake.sentence(nb_words=4, variable_nb_words=True)
    donor.current_medications = fake.sentence(nb_words=4, variable_nb_words=True)
    donor.dolbd = fake.past_datetime()
    # print("THIS", donor.referrees)
    db.session.add(donor)
    db.session.commit()
    donor.update_ndefbd()
    donor.update_status()
    # print("THAT", donor.referrees)
    return donor.id

def subscriber(hosp_id):
    subscriber = Subscriber()
    subscriber.sn = fake.ssn()
    subscriber.email = fake.email()
    subscriber.first_name = fake.first_name()
    subscriber.middle_name = fake.last_name()
    subscriber.last_name = fake.first_name_female()
    subscriber.home_address = fake.address()
    subscriber.hospital_id = hosp_id
    subscriber.city = fake.city()
    subscriber.region = fake.city()
    subscriber.phone1 = fake.phone_number()
    subscriber.phone2 = fake.phone_number()
    subscriber.cni = fake.isbn13()
    subscriber.cni_doi = fake.date_time()
    subscriber.cni_poi = fake.city()
    subscriber.dob = fake.date_time()
    subscriber.pob = fake.city()
    subscriber.gender = random.choice(gender)
    subscriber.blood_group = random.choice(blood_groups)

    subscriber.allergies = fake.sentence(nb_words=4, variable_nb_words=True)
    subscriber.rhesus_factor = random.choice(rhesus_factor)
    subscriber.medical_conditions = fake.sentence(nb_words=4, variable_nb_words=True)
    subscriber.current_medications = fake.sentence(nb_words=4, variable_nb_words=True)

    db.session.add(subscriber)
    db.session.commit()
    return subscriber.id

def hospital():
    hospital = Hospital()
    hospital.name = fake.company()
    hospital.address = fake.address()
    hospital.unit_blood_pile = random.randint(0, 300)
    hospital.city = fake.city()
    hospital.region = fake.city()
    hospital.phone1 = fake.phone_number()
    hospital.phone2 = fake.phone_number()

    db.session.add(hospital)
    db.session.commit()
    return hospital.id

def transfusion(hosp_id, sub_id):

    transfusion = Transfusion()
    transfusion.hospital_id = hosp_id
    transfusion.subscriber_id = sub_id
    transfusion.diagnosis = fake.sentence(nb_words=4, variable_nb_words=True)
    transfusion.hosp_unit = random.choice(hospitalUnits)
    transfusion.id_ut = random.randint(3, 10)
    transfusion.medical_conditions = random.choice(medicalConditions)
    transfusion.hem_level = random.randint(10, 50)
    transfusion.bp_requested = random.choice(bloodTypes)
    transfusion.bp_received = random.choice(bloodTypes)
    transfusion.ubpt = random.randint(10, 50)
    transfusion.onset_time = fake.date_time()
    transfusion.termination_time = fake.date_time()
    transfusion.effect_of_transfusion = fake.sentence(nb_words=5, variable_nb_words=False)
    transfusion.date_requested = fake.date_time()
    transfusion.date_delivered = fake.date_time()
    transfusion.patient_end_status = random.choice(gender)

    db.session.add(transfusion)
    db.session.commit()
    return transfusion.id

def donation(hosp_id, donor_id):

    donation = Donation()
    donation.hospital_id = hosp_id
    donation.donor_id = donor_id
    donation.volume_of_blood = random.randint(1, 20)
    donation.onset_time = fake.date_time()
    donation.termination_time = fake.date_time()
    donation.torfru = fake.date_time()
    
    db.session.add(donation)
    db.session.commit()
    donation.update_donor_dolbd()
    # print("THIS", donation.donor._asdict())
    return donation.id

def defferal(donor_id):

    deferral = Deferral()
    deferral.donor_id = donor_id
    deferral.reason = fake.sentence(nb_words=5, variable_nb_words=False)
    deferral.ndefbd = fake.future_datetime()

    db.session.add(deferral)
    db.session.commit()
    deferral.update_donor_ndefbd()

    return deferral.id


