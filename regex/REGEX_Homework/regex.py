import re
#####################################################################
###################           Section1          #####################
#####################################################################
f = open(r"phone.txt")

string = f.read()
#all_phone_pattern = r".+\s (.+)" #all numbers 
#phone_number_odd_start = r".+\s([13579]\d{2})\s\d{3}-\d{4}"
pattern1_1 =  r"\(([13579]\d{2})\)\s\d{3}-\d{4}"
result1 = re.findall(pattern1_1, string)
print("Section1:Q1.Phone numbers starting with odd numbers: ",result1)

#phone_number_less_than_300 = r"(\w.+?) .+\([012]\d{2}\)"
pattern1_2 = r"^(\w+)\s.+\(([0-2]\d{2})\)"
result2 = [match[0] for match in re.findall(pattern1_2, string,re.MULTILINE)]
print("Section1:Q2.First name only for whose area code is less than 300 : ",result2)

#phone_LNaeiou_LD079 = r"(\w.+?) (\w.+[aeiou])\s .+\-(\d{3}[079])"
pattern1_3 = r"(\w.+?) \w.+[aeiou]\s.+\-\d{3}[079]"
result3 = re.findall(pattern1_3, string)
print("Section1:Q3.All person's first name whose last name ends with vowel and number ends 079 : ",result3)

#####################################################################
###################           Section2          #####################
#####################################################################

f = open(r"logs.txt")

string = f.read()
pattern2_1 = "^(?:Critical|Error)\s+\d{1,2}/\d{1,2}/\d{4}\s+(?:12|1|2|3):\d{2}:\d{2}\sPM\s+(.+?)\s+\d+"
pattern2_2= "^(?:Critical|Error)\s+(\d{1,2}/\d{1,2}/\d{4})\s+\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)\s+TPM\s+"
pattern2_3 = "^(?:Critical|Error)\s+(1/2[4-7]/2020\s+8:\d{2}:\d{2}\sAM)\s+"
result2_1 = re.findall(pattern2_1, string,re.MULTILINE)
result2_2 = re.findall(pattern2_2, string,re.MULTILINE)
result2_3 = re.findall(pattern2_3, string,re.MULTILINE)

print("Section2 : Q1 log entries after 12 PM and before 4 PM", result2_1)
print("Section2 : Q2 Date of all the log entries that have TPM as the Source of the log message", result2_2)
print("Section2 : Q3 Date and Time of all the log entries that have been generated between 24 and 27 of January 2020 and between 8:00:00 and 8:59:59 AM", result2_3)
