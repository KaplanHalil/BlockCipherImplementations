#include <stdio.h>

typedef unsigned long long int bit64;

// 5 bitlik s-kutusu
unsigned char sbox[32]={0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c, 0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17};

// 320 bitlik state
bit64 state[5] = {0};

// Hızlı s-box için kullandığımız temp değeri
bit64 t[5] ={0};

// x : sağa kayma miktarı 
bit64 rotateRight(bit64 girdi, int x){

    bit64 temp ;
    temp = (girdi >> x) ^ (x << (64-x)) ;
    return temp ;
}


void linear(bit64 state[5]){

    bit64 temp0 = rotateRight(state[0],19);
    bit64 temp1 = rotateRight(state[0],28);
    state[0] = state[0] ^ temp0 ^ temp1 ;

    bit64 temp0 = rotateRight(state[1],61);
    bit64 temp1 = rotateRight(state[1],39);
    state[1] = state[1] ^ temp0 ^ temp1 ;

    bit64 temp0 = rotateRight(state[2],1);
    bit64 temp1 = rotateRight(state[2],6);
    state[2] = state[2] ^ temp0 ^ temp1 ;

    bit64 temp0 = rotateRight(state[3],10);
    bit64 temp1 = rotateRight(state[3],17);
    state[3] = state[3] ^ temp0 ^ temp1 ;

    bit64 temp0 = rotateRight(state[4],7);
    bit64 temp1 = rotateRight(state[4],41);
    state[4] = state[4] ^ temp0 ^ temp1 ;

}

void sbox(bit64 x[5]){

    x[0] ^= x[4]; x[4] ^= x[3]; x[2] ^= x[1];
    t[0] = x[0]; t[1] = x[1]; t[2] = x[2]; t[3] = x[3]; t[4] = x[4];
    t[0] =~ t[0]; t[1] =~ t[1]; t[2] =~ t[2]; t[3] =~ t[3]; t[4] =~ t[4];
    t[0] &= x[1]; t[1] &= x[2]; t[2] &= x[3]; t[3] &= x[4]; t[4] &= x[0];
    x[0] ^= t[1]; x[1] ^= t[2]; x[2] ^= t[3]; x[3] ^= t[4]; x[4] ^= t[0];
    x[1] ^= x[0]; x[0] ^= x[4]; x[3] ^= x[2]; x[2] =~ x[2];


}
void p(bit64 state[5], int numberOfPerm){

    for (int i = 0; i < numberOfPerm; i++)
    {
        
    }
    
}

void main(){


    bit64 x[5] = {0};
}