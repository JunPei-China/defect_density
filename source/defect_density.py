# -*- coding: utf-8 -*-
import os,yaml,csv

class Defect(object):
    def __init__(self,name):
        self.__sample_name = name
    
    @property
    def sample_name(self):
        return self.__sample_name
    
    @property
    def cell_volume(self):
        return self.__cell_volume
    @cell_volume.setter
    def cell_volume(self,value):
        self.__cell_volume = value
    
    @property
    def atom_number_in_cell(self):
        return self.__atom_number_in_cell
    @atom_number_in_cell.setter
    def atom_number_in_cell(self,value):
        self.__atom_number_in_cell = value    
    
    @property
    def defect_name(self):
        return self.__defect_name
    @defect_name.setter
    def defect_name(self,value):
        self.__defect_name = value
    
    @property
    def defect_valence_state(self):
        return self.__defect_valence_state
    @defect_valence_state.setter
    def defect_valence_state(self,value):
        self.__defect_valence_state = int(value)
    
    @property
    def carrier_density(self):
        return self.__carrier_density
    def carrier_density(self,value):
        self.__carrier_density = float(value)
    
    @property
    def defect_density(self):
        value = self.carrier_density/abs(self.defect_valence_state)
        return value
    
    @property
    def defect_number_in_cell(self):
        value = self.carrier_density*self.cell_volume/abs(self.defect_valence_state)*1E-24
        return value
    
    @property
    def defect_percent(self):
        value = self.defect_number_in_cell/self.atom_number_in_cell*100
        return value
        
class FileMode(object):
    def read(self):
        CurrentPath=os.getcwd()
        YamlFile=os.path.join(CurrentPath,"input.yaml")

        with open(YamlFile,"r") as f:
            value = yaml.load(f,Loader=yaml.FullLoader)
        return value
    
    def calculate(self):
        parameter = self.read()
        sample_name = parameter["Sample_Name"]
        s = Defect(sample_name)
        s.cell_volume = parameter["Cell_Volume"]
        s.atom_number_in_cell = parameter["Atom_Number_in_Cell"]
        s.defect_name = parameter["Defect_Name"]
        s.defect_valence_state = int(parameter["Defect_Valence_State"])
        s.carrier_density = float(parameter["Carrier_Density"])
        
        print("-"*36+"基本信息"+"-"*36)
        print(" "*4+"本程序由13skeleton编写,如有任何问题，请直接联系邮箱。(J.Pei@foxmail.com)")
        print("-"*36+"输入参数"+"-"*36)
        print("样品名称",s.sample_name)
        print("晶胞体积",s.cell_volume)
        print("晶胞中原子数目",s.atom_number_in_cell)
        print("缺陷名称",s.defect_name)
        print("缺陷价态",s.defect_valence_state)
        if float(s.defect_valence_state) < 0:
            print("每个缺陷会产生%s个空穴"%(abs(s.defect_valence_state)))
        elif float(s.defect_valence_state) > 0:
            print("每个缺陷会产生%s个电子"%(abs(s.defect_valence_state)))
        
        print("载流子浓度",format(s.carrier_density,".3E"))
        print(" ")
        print(" ")
        print(" ")
        
        print("-"*36+"#输出结果"+"-"*36)
        print("缺陷密度",format(s.defect_density,".3E"))
        print("晶胞中缺陷数目",format(s.defect_number_in_cell,".4f"))
        print("缺陷的原子百分含量",format(s.defect_percent,".4f"))
        print("...")
        print("...")
        print("...")
        
        with open("out.csv","w",encoding="utf-8",newline="") as csvfile:
            result = csv.writer(csvfile)
            result.writerow(["#输入参数"])
            result.writerow(["样品名称",s.sample_name])
            result.writerow(["晶胞体积",s.cell_volume])
            result.writerow(["晶胞中原子数目",s.atom_number_in_cell])
            result.writerow(["缺陷名称",s.defect_name])
            result.writerow(["缺陷价态",s.defect_valence_state])
            result.writerow(["载流子浓度",s.carrier_density])
            result.writerow([" "])

            result.writerow(["#输出结果"])
            if float(s.defect_valence_state) < 0:
                result.writerow(["每个缺陷会产生%s个空穴"%(abs(s.defect_valence_state))])
            elif float(s.defect_valence_state) > 0:
                result.writerow(["每个缺陷会产生%s个电子"%(abs(s.defect_valence_state))])
            result.writerow(["缺陷密度",format(s.defect_density,".4e")])
            result.writerow(["晶胞中缺陷数目",format(s.defect_number_in_cell,".4f")])
            result.writerow(["缺陷的原子百分含量",format(s.defect_percent,".4f")])
            
        print("计算完成，输出结果请查看out.csv文件")
if __name__ == "__main__":
    FileMode().calculate()
