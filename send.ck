// another candidate for lamest demo

"localhost" => string hostname;
6449 => int port;

// check command line
if( me.args() ) me.arg(0) => hostname;
if( me.args() > 1 ) me.arg(1) => Std.atoi => port;

// send object
OscSend xmit;

// aim the transmitter
xmit.setHost( hostname, port );

// patch
fun void whole() {
    SinOsc s => JCRev r => dac;
    .5 => r.gain;
    .075 => r.mix;

    // note number
    Std.rand2( 20, 28 ) => float note;
    if ( note % 2 != 0 ) note + 1.0 => note;

    // go up to 127
    while( note < 128 )
    {
        if ( note % 2 == 0 && note == 64 ) Machine.add("send.ck");
        else {
            if ( note % 2 != 0 && note == 127 && maybe ) Machine.add("send.ck");
        }
        // convert MIDI note to hz
        Std.mtof( note ) => s.freq;
        // turn down the volume gradually
        if ( s.gain() > 0 ) .5 - (note/128.0) => s.gain;

        // move up by whole or half step
        if ( maybe ) note + ( 2 - maybe ) => note;
        else note + ( 2 + maybe ) => note;

        // advance time
        125::ms => now;

        xmit.startMsg( "/print", "f f f" );

        (now / ms) % 1000 => xmit.addFloat;
        note => xmit.addFloat;
        s.gain() => xmit.addFloat;
    }
    // turn off s
    0 => s.gain;
    2::second => now;
}

whole();
// wait a bit
2::second => now;
