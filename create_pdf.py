from fpdf import FPDF


def create(names_list, shops_list, path=''):
    try:
        pdf = FPDF()
        pdf.add_page()
        for i in range(len(names_list)):
            shops = shops_list[i]
            name = names_list[i]

            if shops == [['']]:
                print(name + ': отсутствуют данные')
                return

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 5, txt=name, ln=1, align="C")
            for shop in shops:
                # name
                pdf.set_text_color(10, 10, 10)  # black
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 5, txt=shop[0], ln=1)
                # link
                pdf.set_text_color(10, 10, 200)  # blue
                pdf.set_font("Arial", size=8)
                pdf.cell(200, 5, txt=shop[1], ln=1)
                # price
                pdf.set_text_color(10, 10, 10)  # black
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 5, txt=shop[2] + ' p.', ln=1)
                # space
                pdf.cell(200, 5, ln=1)

        pdf.output(path + "Конфигурация.pdf")
    except Exception as exception:
        print(exception)
    import os
    os.system(path + "Конфигурация.pdf")