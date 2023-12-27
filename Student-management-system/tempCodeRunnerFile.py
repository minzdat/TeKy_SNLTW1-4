# Create an empty list to store student information
students = []

# Function to display all students
def display_all_students(students):
    print()
    print("*"*80)
    print("Thông tin tất cả sinh viên:")
    print('.'*80)
    for student in students:
        print("Tên sinh viên: ", student[0].upper())
        print("Mã số sinh viên: ", student[1])
        print('.'*80)

# Function to search for a student by student ID
def search_student_by_id(students, search_id):
    found = False
    for student in students:
        if str(student[1]).find(str(search_id)) != -1:
            found = True
            print("\nThông tin sinh viên có mã số", search_id, ":\n")
            print("\nTên sinh viên: ", " " * 5, student[0].upper())
            print("Mã số sinh viên: ", " " * 3, student[1])
            print("Bảng điểm:")
            print("-" * 90)
            print("{:<20}\t{:^20}\t{:^20}\t{:^20}".format("Tên môn học", "Điểm quá trình", "Điểm cuối kỳ", "Điểm trung bình"))
            for score in student[2]:
                print("{:<20}\t{:^20}\t{:^20}\t{:^20}".format(score[0].upper(), str(score[1]), str(score[2]), str(score[3])))
            break

    if not found:
        print("\nKhông tìm thấy sinh viên có mã số", search_id)

# Function to add a new student
def add_student(students):
    print()
    print("*"*80)
    print("Thêm thông tin sinh viên:")
    print('.'*80)
    student_name = str(input("Nhập tên sinh viên: "))
    student_id = str(input("Nhập mã số sinh viên: "))

    scores = []
    while True:
        subject = str(input("\nNhập tên môn học (hoặc 'q' để dừng): "))
        if subject.lower() == 'q':
            break

        midterm_score = float(input("Nhập điểm quá trình: "))
        final_score = float(input("Nhập điểm cuối kỳ: "))
        average_score = (midterm_score + final_score) / 2
        scores.append((subject, midterm_score, final_score, average_score))

    students.append((student_name, student_id, scores))
    print("\nThêm sinh viên thành công!")

# Function to edit student information
def edit_student(students):
    print("\n" + "*"*80)
    search_id = str(input("Nhập mã số sinh viên cần chỉnh sửa: "))
    for i, student in enumerate(students):
        if student[1] == search_id:
            print("\nThông tin hiện tại của sinh viên có mã số", search_id, ":")
            print("\nTên sinh viên: ", " " * 5, student[0].upper())
            print("Mã số sinh viên: ", " " * 3, student[1])
            print("Bảng điểm:")
            print("-" * 90)
            print("{:<20}\t{:^20}\t{:^20}\t{:^20}".format("Tên môn học", "Điểm quá trình", "Điểm cuối kỳ", "Điểm trung bình"))
            for score in student[2]:
                print("{:<20}\t{:^20}\t{:^20}\t{:^20}".format(score[0].upper(), str(score[1]), str(score[2]), str(score[3])))

            # Prompt user for new information
            new_name = str(input("\nNhập tên mới của sinh viên: "))
            new_id = str(input("Nhập mã số sinh viên mới: "))
            students[i] = (new_name, new_id.replace(str(search_id), str(new_id)), student[2])
            print("\nChỉnh sửa thông tin thành công!")
            break
    else:
        print("\nKhông tìm thấy sinh viên có mã số", search_id)

# Function to delete student information
def delete_student(students):
    print()
    print("*"*80)
    search_id = str(input("Nhập mã số sinh viên cần xóa: "))
    for i, student in enumerate(students):
        if student[1] == search_id:
            del students[i]
            print("\nXóa thông tin sinh viên thành công!")
            break
    else:
        print("\nKhông tìm thấy sinh viên có mã số", search_id)

# Main program
while True:
    print()
    print("*"*80)
    print("Chọn chế độ:")
    print("1. Hiển thị tất cả sinh viên")
    print("2. Tìm kiếm một sinh viên")
    print("3. Xử lý thông tin sinh viên")
    print("4. Thoát")
    
    choice = input("Nhập một chế độ (1-4): ")
    
    if choice == '1':
        display_all_students(students)
    elif choice == '2':
        print()
        print("*"*80)
        search_id = str(input("Nhập mã số sinh viên để tìm kiếm (hoặc 'q' để thoát): "))
        if search_id.lower() != 'q':
            search_student_by_id(students, search_id)
    elif choice == '3':
        print()
        print("*"*80)
        print("Chọn chế độ xử lý thông tin sinh viên:")
        print("   1. Thêm mới thông tin sinh viên")
        print("   2. Chỉnh sửa thông tin sinh viên")
        print("   3. Xóa thông tin sinh viên")
        sub_choice = input("Nhập số chế độ (1-3): ")
        if sub_choice == '1':
            add_student(students)
        elif sub_choice == '2':
            edit_student(students)
        elif sub_choice == '3':
            delete_student(students)
        else:
            print("\nChế độ không hợp lệ. Vui lòng chọn lại.")
    elif choice == '4':
        print("\nKết thúc chương trình.")
        break
    else:
        print("\nChế độ không hợp lệ. Vui lòng chọn lại.")