#this is a Inverse cosine function algorithm
float aacos(float x){
    unsigned char i;
    float ans=x,t1=1,t2=x;x*=x;
    for(i=3;i<51;i+=2){
        t1*=(float)(i-2)/(float)(i-1);
        t2*=x;
        ans+=(t1*t2/(float)i);
    }
    return ans=1.5708-ans;
}
