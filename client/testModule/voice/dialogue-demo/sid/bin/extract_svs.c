/* スーパーベクトル (UBM の平均との差をとらない) を出力 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXLEN 10000


void read_mu_sigma( int dim, int mixture, FILE *gmmfile, double **mu, double **sigma ) {
  int i, k, l;
  char inbuf[MAXLEN], *tp;

  memset(inbuf, 0, MAXLEN);

  for( i = 0; i < 8; i++ ) fgets( inbuf, MAXLEN, gmmfile );

  /* 平均・分散を取り出す */
  for( k = 0 ; k < mixture ; k++ ) {
    for( i = 0; i < 3; i++ ) fgets( inbuf, MAXLEN, gmmfile );
    /* 平均 */
    l = 0;
    tp = strtok( inbuf, " \n" );
    if( tp != NULL ) mu[k][l++] = atof(tp);
    while( tp != NULL ) {
      tp = strtok( NULL, " \n" );
      if( tp != NULL ) mu[k][l++] = atof(tp);
    }

    for( i = 0; i < 2; i++ ) fgets( inbuf, MAXLEN, gmmfile );
    /* 分散 */
    l = 0;
    tp = strtok( inbuf, " \n" );
    if( tp != NULL ) sigma[k][l++] = atof(tp);
    while( tp != NULL ) {
      tp = strtok( NULL, " \n" );
      if( tp != NULL ) sigma[k][l++] = atof(tp);
    }

    fgets( inbuf, MAXLEN, gmmfile );  /* <GCONST> の行 */
  }
}



/* ------------------------- ここから main ------------------------- */

int main( int argc, char *argv[] )
{
  /* Usage */
  if( argc != 4 ) {
    fprintf( stderr, "Usage: $ %s (UBM file) (GMM list) (outfile)\n", argv[0] );
    exit(EXIT_FAILURE);
  }

  FILE *fp_ubm, *fp_list, *fp_gmm, *fp_w;
  int i, k, l;
  char inbuf[MAXLEN];
  int dim, mixture;

  /* 初期化 */
  memset(inbuf, 0, MAXLEN);

  /* GMM リストを開く */
  if( (fp_list = fopen( argv[2], "r" )) == NULL ) {
    fprintf( stderr, "File open error!\n" );
    exit(EXIT_FAILURE);
  }
  fgets( inbuf, MAXLEN, fp_list );

  /* リストの先頭の GMM ファイルを開く */
  if( (fp_gmm = fopen( strtok( inbuf, "\n" ), "r" )) == NULL ) {
    fprintf( stderr, "File open error!\n" );
    exit(EXIT_FAILURE);
  }

  /* GMM から次元数、状態数、各状態分布の平均・分散を取り出す */
  for( i = 0; i < 3; i++ ) fgets( inbuf, MAXLEN, fp_gmm );  /* <VECSIZE> の行 */
  strtok( inbuf, " " );
  dim = atoi(strtok( NULL, " " ));  /* 次元数の取得 */
  for( i = 0; i < 5; i++ ) fgets( inbuf, MAXLEN, fp_gmm );  /* <NUMMIXES> の行 */
  strtok( inbuf, " \n" );
  mixture = atoi(strtok( NULL, " \n" ));  /* 混合数の取得 */
  rewind(fp_list);

  double **mu_ubm, **sigma_ubm, **mu_gmm, **sigma_gmm;

  /* メモリ確保 */
  mu_ubm = (double**)malloc( sizeof(double*) * mixture );
  sigma_ubm = (double**)malloc( sizeof(double*) * mixture );
  mu_ubm[0] = (double*)malloc( sizeof(double) * mixture * dim );
  sigma_ubm[0] = (double*)malloc( sizeof(double) * mixture * dim );
  mu_gmm = (double**)malloc( sizeof(double*) * mixture );
  sigma_gmm = (double**)malloc( sizeof(double*) * mixture );
  mu_gmm[0] = (double*)malloc( sizeof(double) * mixture * dim );
  sigma_gmm[0] = (double*)malloc( sizeof(double) * mixture * dim );
  for( k = 1; k < mixture; k++ ) {
    mu_ubm[k] = mu_ubm[0] + k*dim;
    sigma_ubm[k] = sigma_ubm[0] + k*dim;
    mu_gmm[k] = mu_gmm[0] + k*dim;
    sigma_gmm[k] = sigma_gmm[0] + k*dim;
  }
  if( mu_gmm == NULL || sigma_gmm == NULL || mu_gmm[0] == NULL || sigma_gmm[0] == NULL ) {
    fprintf( stderr, "Error: Memory allocation for mu / sigma failed\n" );
    exit(EXIT_FAILURE);
  }

  /* 入力された GMM の平均・分散を取得し、UBM 平均からの差をとったスーパーベクトルをファイルに書き込む */
  if( (fp_ubm = fopen( argv[1], "r" )) == NULL ) {
    fprintf( stderr, "%s: File open error!\n", argv[1] );
    exit(EXIT_FAILURE);
  }
  if( (fp_w = fopen( argv[3], "wb" )) == NULL ) {
    fprintf( stderr, "%s: File open error!\n", argv[3] );
    exit(EXIT_FAILURE);
  }
  read_mu_sigma(dim, mixture, fp_ubm, mu_ubm, sigma_ubm);
  fclose(fp_ubm);

  while( fgets( inbuf, MAXLEN, fp_list ) != NULL ) {
    fp_gmm = fopen( strtok( inbuf, "\n" ), "r" );
    read_mu_sigma(dim, mixture, fp_gmm, mu_gmm, sigma_gmm);
    fclose(fp_gmm);

    for( k = 0; k < mixture; k++ ) {
      for( l = 0; l < dim; l++ ) mu_gmm[k][l] -= mu_ubm[k][l]; /* UBM 平均からの差 */
      fwrite(mu_gmm[k], sizeof(double), dim, fp_w);
    }
  }

  /* スーパーベクトルの出力（確認用） */
  /*
  for( k = 0; k < mixture-1; k++ ) {
    for( l = 0; l < dim; l++ ) {
      printf("%le ", mu_gmm[k][l]);
    }
  }
  for( l = 0; l < dim-1; l++ ) {
    printf("%le ", mu_gmm[k][l]);
  }
  printf("%le", mu_gmm[k][l]);
  putchar('\n');
  */
  

  return 0;
}
