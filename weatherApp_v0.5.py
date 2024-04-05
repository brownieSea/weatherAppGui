import sys
import requests  # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4  # html page를 불러와서 parsing.해주는 라이브러리
from PyQt5.QtWidgets import *
from PyQt5 import uic  # qt designer에서 만든 ui를 불러오기 위해서 사용
from PyQt5.QtGui import *

form_class = uic.loadUiType('ui/uiWeather.ui')[0]

class naverWeather(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon("img/icon.png"))
        self.statusBar().showMessage("made by brownieSEA")

        self.bttnEnter.clicked.connect(self.weatherSearch)
        self.inputArea.returnPressed.connect(self.weatherSearch)
        # self.inputArea.clicked.connect(self.clearInput)

    def clearInput(self):
        self.inputArea.clear()
    def weatherSearch(self):
        areaTxt = self.inputArea.text()  # 입력한 값 가져오기
        weatherHtml = requests.get(f'https://search.naver.com/search.naver?query={areaTxt}날씨')
        # 네이버에서 한남동 날씨 검색 html 반환. 1개의 문자열로 반환된다.

        #지역이름
        weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')  # hmtl 소스로 만들기
        areaResult = weatherSoup.find('h2', {"class":"title"}).text  # 일치하는 정보를 찾아 제일 처음 일치하는 값중 텍스트 값을 반환. 지역 이름 가져오기
        areaResult = areaResult.strip()

        #현재온도
        TemperatureTxt = weatherSoup.find('div', {'class':'temperature_text'}).text
        TemperatureTxt = TemperatureTxt[6:].strip()  # 6번째 글자부터 슬라이싱 하고 양쪽 공백 제거

        #어제와 비교
        yesterday = weatherSoup.find('p', {'class':'summary'}).text
        yesterday1 = yesterday[:15].strip()

        #날씨
        tempStatus = weatherSoup.find('span', {'class':'weather before_slash'}).text
        tempStatus = tempStatus.strip()

        #체감온도
        Tendency = weatherSoup.find('dd', {'class':'desc'}).text

        todayInfo = weatherSoup.select('ul.today_chart_list>li')  # ul class=today_chart_list 아래에 있는 li tag 사용한 애들을 리스트로 반환

        #미세먼지
        dust1Info = todayInfo[0].find('span', {'class':'txt'}).text.strip()  #todayInfo 정보중 첫번째 인덱스(첫번째 li)에서 데이터 가져오기

        #초미세먼지
        dust2Info = todayInfo[1].find('span', {'class':'txt'}).text.strip()

        #자외선
        uvInfo = todayInfo[2].find('span', {'class':'txt'}).text.strip()

        #일출/일몰
        sunInfo = todayInfo[3].find('strong', {'class':'title'}).text.strip()
        sunTime = todayInfo[3].find('span', {'class':'txt'}).text.strip()

        self.todayArea.setText(areaResult)  # 조회지역 todayArea
        self.todayTemper.setText(TemperatureTxt)  # 현재온도 todayTemper
        self.compYday.setText(yesterday1)  # 어제와의 온도 비교 compYday
        self.todayTendency.setText(Tendency)  # 체감온도 todayTendency
        self.todayDust1.setText(dust1Info)  # 미세먼지 todayDust1
        self.todayDust2.setText(dust2Info)  # 초미세먼지 todayDust2
        self.todayUV.setText(uvInfo)  # 자외선지수 todayUV
        self.txtSun.setText(sunInfo)  # 일출/일몰 txtSun
        self.todaySunTime.setText(sunTime)   # 일출/일몰 시간  todaySunTime
        self.setWeatherImg(tempStatus)  # 날씨 이미지 출력 함수 호출

    def setWeatherImg(self, tempStatus):  #날씨에 따른 이미지 출력
        if "맑음" in tempStatus:
            pixmap = QPixmap('img/sun.png')
        elif "구름" or "흐림" in tempStatus:
            pixmap = QPixmap('img/cloud.png')
        elif "눈" in tempStatus:
            pixmap = QPixmap('img/snow.png')
        elif "비" in tempStatus:
            pixmap = QPixmap('img/rain.png')
        else:
            self.imgWeather.setText(tempStatus)
        self.imgWeather.setPixmap(QPixmap(pixmap))

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 모든 응용프로그램이 작동하려면 QApplication 객체 필요.
    naverWin = naverWeather()
    naverWin.show()
    sys.exit(app.exec_())  # 창을 닫아주는 명령어