

trigger AccountTrigger on Account (before insert)
{

	Account a = trigger.New[0];

	Contact listContacts = [SELECT ID FROM CONTACT WHERE ACCOUNTID =:a.id];

	for(Contact c : listContacts){
		
		c.City__c = a.City__c;
		
		UPDATE c;	
	}
	
}