//
// Created by Jurio on 2020/3/4.
//1.方法1：通过相切条件列方程求解圆心坐标及半径
//2.定义最大内切圆半径为R=1,圆心坐标(X,Y)=(0,0)
//3.计算5组数据后发现当圆填充在最大内切圆和正方形的空隙中时面积最大，合理外推各结论始终成立
//4.第m个圆的半径和圆心数据存在数组里,根据对称性分奇偶讨论
//5.由于水平有限及方程解法的局限性,理论上只能求出m<30的情况

#include <iostream>
#include <cmath>
using namespace std;

int X = 0,Y = 0,R = 1; //初始化第1个圆的数据
float x[50],y[50],r[50]; //定义其他m-1个圆存放数据的数组

//一元二次方程求解函数
float Fun(float a,float b,float c){
    float x1,x2;
    x1=(-b+sqrt(b*b-4*a*c))/(2*a);
    x2=(-b-sqrt(b*b-4*a*c))/(2*a);
    if(0<x1 && x1<1)
        return x1;
    else
        return x2;
}
//获取第2个圆的数据
void circle2(){
    r[0] = Fun(1,-6,1);
    x[0] = 1-r[0]; y[0] = 1-r[0]; //第2个圆
}
//根据对称性,已知第一象限的圆求其他三个象限圆的数据
void one_to_other_three(int m){
    x[m+1] = -x[m];  y[m+1] = y[m];  r[m+1] = r[m]; //第二象限
    x[m+2] = -x[m];  y[m+2] = -y[m]; r[m+2] = r[m]; //第三象限
    x[m+3] = x[m];  y[m+3] = -y[m];  r[m+3] = r[m]; //第四象限
}
//当m=4的奇数倍，即4,12,20时
void odd_time(int n){
    float temp;
    temp = Fun(2+2*y[n-4]-2*r[n-4],-4*x[n-4],1-2*y[n-4]);
    r[n] = temp*temp;
    x[n] = 2*temp;
    y[n] = 1-r[n];
}
//当m=4的偶数倍，即8,16,24时
void even_time(int k){
    r[k] = r[k-4];
    x[k] = y[k-4];
    y[k] = x[k-4];
}

int main()
{
    circle2();
    for(int i=1; i<6; i++){
         if(i%2 == 1)
             odd_time(4*i);
         else
             even_time(4*i);
    }
    for(int j=0; j<7; j++)
         one_to_other_three(4*j);

    cout<<"x1="<<X<<'\t'<<"y1="<<Y<<'\t'<<"r1="<<R<<endl;
    for(int h=2; h<30; h++){
         cout<<"x"<<h<<"="<<x[h-2]<<'\t';
         cout<<"y"<<h<<"="<<y[h-2]<<'\t';
         cout<<"r"<<h<<"="<<r[h-2]<<'\t'<<endl;
    }

    return 0;
}
