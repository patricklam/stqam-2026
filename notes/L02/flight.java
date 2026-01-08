// Meszaros, p. 471
// not self-checking
public void testRemoveFlightLogging_NSC() {
 // arrange:
 FlightDto expectedFlightDto=createRegisteredFlight();
 FlightMgmtFacade facade=new FlightMgmtFacadeImpl();
 // act:
 facade.removeFlight(expectedFlightDto.getFlightNo());
 // assert:
 // have not found a way to verify the outcome yet
 //  Log contains record of Flight removal
}
