import csv

import numpy as np

from config.settings import DATA_DIRS


class Mynumpy:
    # 1. 서울시 지역별 영유아(5세이하) 현황
    def infantspop(self):
        f = open(DATA_DIRS[0]+'\\age3.csv');
        data = csv.reader(f);
        next(data);
        data = list(data);
        reg = [];
        pop = [];
        result = [];
        for row in data:
            ypop = np.array(row[3:9], dtype=int); #0~5세 데이터 추출
            pop = int(np.sum(ypop));
            reg = row[0].split(' ')[1];
            result.append([reg,pop]);
        return result;

    # 2. 서울시 지역별 3년간(18~20) 인구증가율
    def popgrowrate(self):
        f = open(DATA_DIRS[0]+'\\age4.csv');
        data = csv.reader(f);
        next(data);
        data = list(data);

        reg=[];
        irate=[];
        result=[];
        for row in data:
            rdata = (int(row[27]) - int(row[1]));  # 인구 증가량
            irate = round((rdata / int(row[1])) * 100,3) # 증가율
            reg = row[0].split(' ')[1];
            result.append({
                'name': reg,
                'data': [irate]   ## highcharts 형식에 맞추기 위해 [] 사용
            });
        print(result);
        return result;

    #서울시 특정지역과 인구분포가 유사한 지역
    def searchregion(self,region):
        f = open(DATA_DIRS[0]+'\\age2.csv');
        data = csv.reader(f);  ## _csv.reader type
        next(data);
        data = list(data);  ## list type으로 바꿈

        home = None;
        home2 = None;
        popspr = None;
        result = {};
        reg = [];
        result3 = [];
        # 특정 지역의 연령 별 비율
        for row in data:
            if region in row[0]:
                home = np.array(row[3:], dtype=int);
                home2 = home / int(row[2]);
                reg= row[0][0:row[0].find('(')];
                popspr = home2.tolist()
            result = {
                    'name': reg,
                    'data': popspr
            }
        # 모든 지역의 연령 별 비율을 구한다.
        min = 99999
        reg2=[];
        popspr2=None;
        result2={};
        for row in data:
            away = np.array(row[3:], dtype=int);
            away2 = away / int(row[2]);
            s = np.sum(np.abs(home2 - away2));
            if region not in row[0] and s < min:
                min = s;
                reg2 = row[0][0:row[0].find('(')];
                popspr2 = away2.tolist();
            result2 = {
                'name': reg2,
                'data' : popspr2
            }
        result3.append(result)
        result3.append(result2)
        print(result3);
        return(result3);

if __name__ == '__main__':
    Mynumpy().searchregion('신도림');