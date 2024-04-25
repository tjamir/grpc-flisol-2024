package main

import (
	api "bank-server/internal/api"
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/timestamppb"
)

var (
	port = flag.Int("port", 50051, "The server port")
)

func main() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	reflection.Register(s)
	bank := &bank{
		accounts: map[string]*account{},
		accountId: 1,
		transactionId: 1,
	}
	
	api.RegisterClerkBankServiceServer(s, bank)
	api.RegisterClientBankServiceServer(s, bank)
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
	
	
}

type transaction struct{
	id string
	amount float32
	time time.Time

}
type account struct {
	id string
	password string
	balance float32
	holder string
	transactions []transaction
}



type bank struct {
	api.UnimplementedClientBankServiceServer
	api.UnimplementedClerkBankServiceServer
	accounts map[string]*account
	accountId int
	transactionId int
}

func (b *bank) CreateAccount(ctx context.Context, in *api.CreateAccountRequest) (*api.CreateAccountResponse, error) {
	id := b.accountId
	b.accountId++

	formattedId := fmt.Sprintf("%06d", id)
	b.accounts[formattedId] = &account{
		id: formattedId,
		password: in.Password,
		balance: 0,
		holder: in.Name,
		transactions: []transaction{},
	}

	return &api.CreateAccountResponse{
		AccountId: formattedId,
		Name: in.Name,
	
	}, nil

}

func (b *bank) DoTransaction(ctx context.Context, in *api.TransactionRequest) (*api.TransactionResponse, error) {
	account, ok := b.accounts[in.AccountId]
	if !ok {
		return nil, status.Error(codes.NotFound, "account not found")
	}
	if in.Action == api.Action_ACTION_DEPOSIT {
		return b.deposit(ctx, account, in)
	} else if in.Action == api.Action_ACTION_WITHDRAWAL {
		return b.withdraw(ctx, account, in)
	}
	return nil, status.Error(codes.InvalidArgument, "invalid action")
}

func (b *bank) deposit(ctx context.Context, account *account, in *api.TransactionRequest) (*api.TransactionResponse, error){
	if in.Amount <= 0 {
		return nil, status.Error(codes.InvalidArgument, "invalid amount")
	}
	id := b.nextTransactionId()
	account.balance += in.Amount
	account.transactions = append(account.transactions, transaction{
		id: id,
		amount: in.Amount,
		time: time.Now(),
	})
	return &api.TransactionResponse{
		Transaction: &api.Transaction{
			Id: id,
			Amount: in.Amount,
			Time: timestamppb.New(time.Now()),
		},
		AccountBalance: account.balance,

	}, nil
}

func (b *bank)withdraw(ctx context.Context, account *account, in *api.TransactionRequest) (*api.TransactionResponse, error){
	if in.Amount <= 0 {
		return nil, status.Error(codes.InvalidArgument, "invalid amount")
	}
	if account.balance < in.Amount {
		return nil, status.Error(codes.FailedPrecondition, "insufficient funds")
	}
	id := b.nextTransactionId()
	account.balance -= in.Amount
	account.transactions = append(account.transactions, transaction{
		id: id,
		amount: -in.Amount,
		time: time.Now(),
	})
	return &api.TransactionResponse{
		Transaction: &api.Transaction{
			Id: id,
			Amount: -in.Amount,
			Time: timestamppb.New(time.Now()),
		},
		AccountBalance: account.balance,
	}, nil
}

func (b *bank) Transfer(ctx context.Context, in *api.TransferRequest) (*api.TransactionResponse, error){
	source, hasSource := b.accounts[in.SourceAccountId]
	target, hasTarget := b.accounts[in.TargetAccountId]

	if !hasSource {
		return nil, status.Error(codes.NotFound, "source account not found")
	}
	if !hasTarget {
		return nil, status.Error(codes.NotFound, "target account not found")
	}

	if in.Value <= 0 {
		return nil, status.Error(codes.InvalidArgument, "invalid value")
	}

	if source.balance < in.Value {
		return nil, status.Error(codes.FailedPrecondition, "insufficient funds")
	}

	if source.password != in.Password {
		return nil, status.Error(codes.PermissionDenied, "invalid password")
	}

	tx, err := b.withdraw(ctx, source, &api.TransactionRequest{
		AccountId: in.SourceAccountId,
		Action: api.Action_ACTION_WITHDRAWAL,
		Amount: in.Value,
	})
	if err != nil {
		return nil, err
	}
	_, err = b.deposit(ctx, target, &api.TransactionRequest{
		AccountId: in.TargetAccountId,
		Action: api.Action_ACTION_DEPOSIT,
		Amount: in.Value,
	})
	if err != nil {
		return nil, err
	}
	return tx, nil
}

func (b *bank) Statement(ctx context.Context, in *api.BankStatementRequest) (*api.BankStatementResponse, error){
	account , exists := b.accounts[in.AccountId]
	if !exists {
		return nil, status.Error(codes.NotFound, "account not found")
	}
	if account.password != in.Password {
		return nil, status.Error(codes.PermissionDenied, "invalid password")
	}
	var transactions []*api.Transaction
	for _, t := range account.transactions {
		transactions = append(transactions, &api.Transaction{
			Id: t.id,
			Amount: t.amount,
			Time: timestamppb.New(t.time),
		})
	}
	return &api.BankStatementResponse{
		Amount: account.balance,
		Transactions: transactions,
	}, nil
	
}


func (b *bank) nextTransactionId() string {
	defer func(){
		b.transactionId++
	}()
	return fmt.Sprintf("%06d", b.transactionId)
}