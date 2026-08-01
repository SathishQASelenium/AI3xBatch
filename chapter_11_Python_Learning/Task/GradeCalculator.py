# ✅ Grade Calculator:
# Write a program that calculates and displays the letter grade
# for a given numerical score (e.g., A, B, C, D, or F)
# based on the following grading scale
# A: 90-100
# B: 80-89
# C: 70-79
# D: 60-69
# F: 0-59

score = int(input("Enter the numerical score: "))

if score >= 90 and score <= 100:
    grade = "A"
elif score >= 80 and score <= 89:
    grade = "B"
elif score >= 70 and score <= 79:
    grade = "C"
elif score >= 60 and score <= 69:
    grade = "D"
elif score >= 0 and score <= 59:
    grade = "F"

print("The letter grade is:", grade)