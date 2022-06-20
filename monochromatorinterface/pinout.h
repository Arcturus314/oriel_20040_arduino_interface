/* Kaveh Pezeshki
 * 06/20/2022
 * Pinout information for 'USER IO' header on Oriel 20040 and associated pin mapping
 * Pinout information taken from: https://files.elektroda.pl/782593,20050.html
 * 
 * Relevant pins on DB-15 are (oriel):
 *  7: 5V/100mA supply
 *  9: Motor half/full
 *  10: Motor EN
 *  11: Motor FWD lim
 *  12: Motor REV lim # THIS IS AN OUTPUT!
 *  13: Motor step pulse # THIS IS AN OUTPUT!
 *  14: Motor FWD/REV
 *  15: Motor GND
 */

 #ifndef pinout_h
 #define pinout_h

struct db15_struct {
    int halffull = 9;
    int en = 10;
    int fwdlim = 11;
    int revlim = 12;
    int steppulse = 13;
    int fwdrev = 14;
} db15;


 #endif
 