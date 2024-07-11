# 火炮内弹道数据集及应用
## 仓库简介
本代码仓库由一个整合了中口径及以上（>=57mm）国产火炮的关键内-外弹道学技战术指标的数据集，及一些以Python编写的应用程序组成。

## 库结构说明
* [**readme.md**](readme.md) 中英文说明文件
* [**arty.json**](arty.json) 以json格式编码的数据集文件
* [**ballistic_parser.py**](ballistic_parser.py) 以Python语言编写的数据集序列化程序
* [**propulsion_graph.py**](propulsion_graph.py) 以Python语言编写的，展示装药比与初速关系的程序

## 文件格式说明
数据集的全部文档均以UTF-8格式编码。若为特殊申明，默认类型为字符串。若项目 __加粗__ 则为必填项。若涉及到角度的表示，均以度数为单位，采用十进制小数表示，不支持以度分秒计。


## 数据集格式说明
- __guns__:火炮列表
    - __name_cn__:中文名称。
    - __name_en__:英文名称。
    - comment: 备注；描述性文字。
    - __caliber_mm__:（浮点数）以毫米计量的口径（阳线顶所在的圆半径），浮点数。内弹道和外弹道计算中常以该直径对应的圆半径作为弹/膛等效截面积。
    - max_elev_deg:（浮点数）炮身与炮架形成的最大仰角。
    - min_elev_deg:（浮点数）炮身与炮架形成的最小仰角。俯角以负数计算。
    - firing_arc_left_deg:（浮点数）下了大架或驻锄的情况下，炮身向左侧能够旋转的最大角度。
    - firing_arc_right_deg:（浮点数）下了大架或驻锄的情况下，炮身向右侧能够旋转的最大角度。
    - __shells__:弹药列表
        - __name_cn__:中文名称。
        - __name_en__:英文名称。
        - comment:备注；描述性文字。
        - __shell_types__:弹药类型标签，以半角（英文）逗号隔开。
        - __shot_mass_kg__:（浮点数）以公斤计量的表定弹重。
        - chamber_length_dm:（浮点数）以分米（0.1米）计量的实际炮膛长度。
        - chamber_volume_L: (浮点数）以公升（立方分米）计量的火炮实际炮膛容积，即弹后可燃物及火药及其燃气气体可及空间的全部容积。
        - travel_dm: (浮点数）以分米计算的弹药全部闭气行程。
        - i_43:（浮点数）无量纲，以1943年阻力定律计算的弹头弹形系数。详见说明部分。
        - c_43:（浮点数）以1943年阻力定律计算的弹道系数。单位为`10^-9 m^2/kg`。详见说明部分。
        - __loads__:装药划分列表
            - name_cn:中文名称。若未标注，默认“正常装药”。
            - name_en:英文名称。若未标注，默认“Normal Charge"。
            - comment:备注；描述性文字。
            - __muzzle_velocity_m/s__:该装填条件下的弹药初速。
            - max_avg_pressure_kgf/sqcm:该装填条件下的以千克力每平方厘米计量的最大膛内（空间）平均压强。见说明。
            - i_43:（浮点数）无量纲，该装填条件下，以1943年阻力定律计算的弹头弹形系数。详见说明部分。
            - c_43:（浮点数）该装填条件下，以1943年阻力定律计算的弹道系数。单位为`10^-9 m^2/kg`。详见说明部分。
            - __charges__:装药细分列表。
                - name_cn:中文名称。若未标注，默认“主装药”。
                - name_en:英文名称。若未标注，默认“Main Charge"。
                - comment:备注；描述性文字。
                - __charge_type__:火药类型。
                - __charge_mass_kg__:（浮点数）以公斤计量的火药装填量。
                - __amount__:（整形）该药包的数目，若未标注，默认1。

## 一些需要特别说明的问题
- __关于压强的单位__：\
    由于国内内弹道学继承苏联的衣钵，采用的是“公斤-分米-秒”计量系统，早期内弹道文献中常以“公斤（力）每平方厘米”计量压强，其与现今利用的国际单位制中的“帕斯卡”的对应关系为，`10 kgf/cm^2=0.9805MPa`。因其数值上接近，部分文献选择直接记作`1MPa`，但实际计算中仍然隐含了一步涉及重力加速度的转化。如果这里仿照后者直接记作`MPa`则会引入大约2%的影响。虽然客观而言，由于火炮膛压受环境温度影响很大，火药燃速系数的不确定性也高于该处理引入的误差，但本着对历史数据实事求是的态度，这里仍然以原单位表征，以期更好体现内弹道设计过程中的目标指标。
- __关于选择最大平均压强作为火炮压强表征指标__：\
    在本数据集参考的时间跨度内，我国内弹道设计的惯例是以某火炮的等效直膛模型下的，沿膛底距离取平均（或近似等价地，对原炮按容积取的平均）的压强控制在某一特定水平为目标。这与我国长期采用的苏系0维内弹道模型有关，同时也是当时弹道表上的变元。根本上来说，该指标能更好的反应全炮膛的受力状态，也和火炮的全炮重等技战术指标更直接相关。这与常取膛底压强（即对某一时刻而言其膛内压强的极大值）作变量及设计指标的西方有很大不同。这两个指标之间只能通过内弹道理论计算进行转化，因此我国很多火炮仅有“计算膛底压强最大值”一个近似指标，其明显存在向上取整的问题，参考价值不如设计平均压强。此外，我国内弹道标准测试条件也与西方也有差异，因此，即使选择膛底压强也不能更加方便比较，故作此选择。
- __43年阻力定律下的两种阻力系数__：\
    我国的外弹道实践过程中，对于旋转体炮弹以及火箭弹，常使用1943年阻力定律。该阻力定律给定了（当时）常见形状的榴弹炮弹，其在标准气象条件下的海平面上，所受的空气阻力与动压的比例随马赫数变化的函数。对于其他形状的弹体，常常可以引入一个“弹形系数”，用于描述该外形弹体和定律所规定的弹体，同一条件下的空气阻力之比。这个系数即为第一种表达形式，“弹型系数” `i_43`，这是一个无量纲量。在微型计算机普及前，为了简便计算，以及制表查表方便，常常还将影响空气阻力加速度大小的其他两个因素，即弹重和口径，也计入该系数，即为第二种表达形式，“弹道系数” `c_43`。这里参考我国射表以及外弹道相关文献，取`10^-9 m^2/kg`为单位，此时二者之间的关系有`i_43 <1> = c_43 <10^-9 m^2/kg> * 1000 * m <kg> / (d <mm>)^2`，`<>`内为各项的量纲，`d,m`分别为口径与弹重（均含在所整理项目中）。\
    两种阻力系数各有优缺点：对于弹型系数，其数值大小能更直观的体现出弹药（比较同样速度区间其他设计）的空气动力学设计水平；对于弹道系数，其数值大小则直接反应了弹药受空气阻力影响的加速度水平，与例如“每公里速降”等弹药的外弹道性能指标更直接挂钩。这点在遇到例如超速脱壳穿甲弹等弹重系数较高或尾翼破甲弹等阻力较大的弹种时体现的较为明显。在数据集中，我们选择保留了原始材料对于各个弹种标注哪个系数的对应关系，如果有需求可以在读取中进行转化。例如，在随附的以Python实现的序列化程序中，即采用了“对于同时有两种阻力系数数据的弹种，优先采取弹型系数，其次当弹型系数未有列出时则通过弹道系数转化所得”的策略，可以提供参考。
- __弹种与装药分别列的空气阻力系数__：\
    由于实际上，非“典型外形”的弹药的实际空气阻力与马赫数的比例并不能通过常数放缩1943年阻力定律来表征，因此任何特定的空气阻力系数实际表征的是以某一特定弹速，射角发射的弹道全过程中所受阻力的平均值。在曲射弹药设计的层面，常常取得到最大射程（满足最大射程指标）的弹道所对应的阻力系数，作为该弹的典型值。但计算射表时，需要根据实际速度区间对其修正。这意味着对于任何特定的装药条件、射角以及外弹道环境均需要对其重新核算。因此，在本数据集中，在弹种性质属性下记录的为第一种“典型”阻力系数，在有射表或材料支撑时，在装药性质属性下记录的为第二种经过修正的，在该装药条件下，（在标准炮兵气象条件的海平面）以45度（或达到最大射程对应的）射角射击时，达到射表标定的射程所对应的空气阻力系数。

## 联系作者
翟锦鹏，电子邮箱：914962409@qq.com
___

# In English:
## Introduction for the Repository:
This repository consists of a dataset detailing key interior and exterior ballistic parameters for domestic artillery pieces of medium caliber and above (>=57mm), and various Python scripts demonstrating some applications. 

## Structure of the Repository:
* [**readme.md**](readme.md) bi-lingual readme file
* [**arty.json**](arty.json) the dataset, encoded in json.
* [**ballistic_parser.py**](ballistic_parser.py) serialization script in Python.
* [**propulsion_graph.py**](propulsion_graph.py) a Python script for the visualizaiton of charge mass ratio and its influence on projectile velocity.

## File Format:
All files are encoded in UTF-8 format. Unless otherwise specified, all fields in the dataset should be of type string. Mandatory fields are distinguished here with __bold__ font. If angular measures are involved, the only measurement that is supported is decimal degree. 

## Dataset Format:

## Some Issues of Particular Note:
- __On the Unit of Pressure__:\
    Chinese tradition of interior ballistics follows that of the Soviet, including the use of "kilogram-decimeter-second" system of measurement. In particular, the choice of "kilogram-per square centimeter" as a unit of pressure is to be implicitly understood as "kilogram-force per square centimeter", with an approximate correspondence to modern units of `10 kgf/cm^2 = 0.9805 MPa`. Although, it must be noted that the precision of measurement does not imply accuracy, as the pressure developed in bore is highly sensitive to both propellant burn rate variations and initial powder temperature. For less rigorous purposes, approximating it as `0.1 MPa` introduce less than 2% of inaccuracy. Values recorded in the dataset have not been converted from their original measurement, but the user is warned that these measurement can only be considered as "nominal". 
- __On the Choice of Peak Mean Bore Pressure__:\
    For the period under consideration, Chinese domestic ballistic tradition is to reference the length-averaged pressure of a constant-bore-diameter gun with equivalent chamber volume, or equivalently, the volume-averaged pressure of the real gun, in the design phase. As a descriptive parameter of the gun system, the mean bore pressure better reflects the actual level of pressure encountered in most part of the bore, thus better correlating to tactical-technical characteristics such as total bore weight. This is in contrast to Western systems of interior ballistics, where the reference pressure is the peak breech pressure. This parameter reflects the highest level encountered in bore, and is thus not comparable to the values as presented in this table. These two measures can be related through the theory of interior ballistics, and that accounts for the presence of a "calculated peak breech pressure" in the sources consulted for this dataset. However, the precision of such information appears poor, as these values are invariably rounded up and listed as "no greater than", and thus serve no better for ballistic comparison. Therefore, the choice of peak mean bore pressure is selected in consideration of all the aforementioned factors.
- __On the Two Ballistic Coefficients__:\
    The 1943 drag curve is used in domestic Chinese exterior ballistics practices in the calculation of point-mass trajectory for rotating shell and rockets. The 1943 drag curve gives the ratio of drag forces to the dynamic pressure, for a given reference shape that corresponds to a (back then) nominal howitzer round, across a range of Mach numbers. For any other shape, a dimensionless factor, the "shape coefficient", denoted `i_43`, is used to scale the drag such that the effect is approximately the same within a specific range of conditions. Previous to the proliferation of micro-computers, for the sake of facilitating a solution via look-up tables, it is common practice to also factor in the two other variables influencing the acceleration as experienced by the projectile, namely the caliber and the weight of the shell, as the "ballistic coefficient", denoted `c_43`, and expressed in units of `10^-9 m^2/kg` to bring the numeric value close to unity. The two can be converted from each other as: `i_43 <1> = c_43 <10^-9 m^2/kg> * 1000 * m <kg> / (d <mm>)^2`，where `<>` denotes dimension，`d,m` for caliber and shell mass.\
    Comparatively, the shape coefficient is more conducive to demonstrating the relative aeroballistic efficiency of a particular shell's shape design independent of other variables, while the ballistic coefficient relates more directly to the deceleration as a consequence of aeroballistic effects, closely related to the exterior ballistic performance of a shell. When both data are available, we have elected to remain faithful to the source and preserve both without preference. The approach of the bundled Python serizalization script is provided for reference, which attempts to read and store the shape coefficient, converting from ballistic coefficient as necessary, when either is specified in the dataset.
- __Ballistic Coefficient Tabulated Per Charge__:
    In actuality, each particular shape of shell is associated with a particular drag curve that may be dissimilar to the 1943 drag curve. Therefore, a specific ballistic coefficient is only correct, on an average sense, for a particular trajectory. For this dataset, the tabulated ballistic coefficient is chosen such that the calculated trajectory matches the actual trajectory for when maximum range (when shooting a target at the same altitude as the gun) is achieved, for this charge loading, in keeping with the sources. Such detailed design information is, unfortunately, not always available.

## Contact Me:
Jinpeng Zhai，Email: 914962409@qq.com
